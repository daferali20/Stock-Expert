# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import logging

from ..core.database import get_db
from ..core.security import security_service
from ..core.config import settings
from ..models.user import User, UserRole
from ..schemas.user import (
    UserCreate, 
    UserLogin, 
    TokenResponse, 
    UserResponse,
    ApiKeyResponse
)

logger = logging.getLogger(__name__)
router = APIRouter()

# ============================================
# مسارات المصادقة الأساسية
# ============================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    تسجيل مستخدم جديد في النظام
    """
    # التحقق من وجود البريد الإلكتروني
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مسجل بالفعل"
        )
    
    # التحقق من وجود اسم المستخدم
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="اسم المستخدم موجود بالفعل"
        )
    
    # تشفير كلمة المرور
    hashed_password = security_service.hash_password(user_data.password)
    
    # إنشاء المستخدم
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=UserRole.USER,  # المستخدم العادي
        is_active=True,
        is_verified=False  # سيتم التحقق لاحقاً عبر البريد
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"✅ تم تسجيل مستخدم جديد: {new_user.username} ({new_user.email})")
    
    # إرسال بريد التحقق (سنضيفه لاحقاً)
    # await send_verification_email(new_user.email)
    
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    تسجيل الدخول والحصول على توكنات الوصول
    """
    # البحث عن المستخدم
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # التحقق من كلمة المرور
    if not security_service.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # التحقق من أن المستخدم نشط
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="الحساب غير نشط. يرجى التواصل مع الدعم"
        )
    
    # تحديث وقت آخر تسجيل دخول
    user.last_login = datetime.utcnow()
    db.commit()
    
    # إنشاء التوكنات
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "username": user.username,
        "role": user.role.value
    }
    
    access_token = security_service.create_access_token(token_data)
    refresh_token = security_service.create_refresh_token(token_data)
    
    logger.info(f"✅ تسجيل دخول: {user.username}")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/login/oauth2", response_model=TokenResponse)
async def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    تسجيل الدخول باستخدام OAuth2 (لتوافق مع Swagger UI)
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة"
        )
    
    if not security_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="الحساب غير نشط"
        )
    
    # تحديث وقت آخر تسجيل دخول
    user.last_login = datetime.utcnow()
    db.commit()
    
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "username": user.username,
        "role": user.role.value
    }
    
    access_token = security_service.create_access_token(token_data)
    refresh_token = security_service.create_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    تحديث توكن الوصول باستخدام توكن التحديث
    """
    try:
        # فك تشفير توكن التحديث
        payload = security_service.decode_token(refresh_token)
        
        # التحقق من نوع التوكن
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="توكن غير صالح"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="المستخدم غير موجود أو غير نشط"
            )
        
        # إنشاء توكنات جديدة
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role.value
        }
        
        new_access_token = security_service.create_access_token(token_data)
        new_refresh_token = security_service.create_refresh_token(token_data)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception as e:
        logger.error(f"خطأ في تحديث التوكن: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="توكن غير صالح أو منتهي الصلاحية"
        )

@router.post("/logout")
async def logout(
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    تسجيل الخروج (من جانب العميل)
    """
    # في حالة استخدام Blacklist للتوكنات، يمكن إضافة التوكن إلى القائمة السوداء
    logger.info(f"🚪 تسجيل خروج: {current_user.get('username')}")
    
    return {
        "message": "تم تسجيل الخروج بنجاح",
        "status": "success"
    }

# ============================================
# مسارات إدارة الحساب
# ============================================

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    الحصول على معلومات المستخدم الحالي
    """
    user = db.query(User).filter(User.id == current_user.get("user_id")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    return user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: dict,  # سنستخدم Schema لاحقاً
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    تحديث معلومات المستخدم الحالي
    """
    user = db.query(User).filter(User.id == current_user.get("user_id")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    # تحديث الحقول المسموح بها
    if "full_name" in user_update:
        user.full_name = user_update["full_name"]
    
    if "email" in user_update:
        # التحقق من أن البريد غير مستخدم
        existing = db.query(User).filter(
            User.email == user_update["email"],
            User.id != user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="البريد الإلكتروني مستخدم بالفعل"
            )
        user.email = user_update["email"]
    
    if "password" in user_update:
        user.hashed_password = security_service.hash_password(user_update["password"])
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"✏️ تم تحديث معلومات المستخدم: {user.username}")
    
    return user

@router.post("/me/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    تغيير كلمة المرور
    """
    user = db.query(User).filter(User.id == current_user.get("user_id")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    # التحقق من كلمة المرور القديمة
    if not security_service.verify_password(old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="كلمة المرور الحالية غير صحيحة"
        )
    
    # تحديث كلمة المرور
    user.hashed_password = security_service.hash_password(new_password)
    db.commit()
    
    logger.info(f"🔑 تم تغيير كلمة المرور للمستخدم: {user.username}")
    
    return {
        "message": "تم تغيير كلمة المرور بنجاح",
        "status": "success"
    }

# ============================================
# مسارات مفاتيح API
# ============================================

@router.post("/me/api-key", response_model=ApiKeyResponse)
async def generate_api_key(
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    إنشاء مفتاح API جديد للوصول البرمجي
    """
    user = db.query(User).filter(User.id == current_user.get("user_id")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    # إنشاء مفتاح API جديد
    api_key = security_service.generate_api_key()
    hashed_key = security_service.hash_api_key(api_key)
    
    user.api_key = hashed_key
    db.commit()
    
    logger.info(f"🔑 تم إنشاء مفتاح API للمستخدم: {user.username}")
    
    return {
        "api_key": api_key,  # يظهر مرة واحدة فقط
        "message": "تم إنشاء مفتاح API بنجاح. يرجى حفظه في مكان آمن"
    }

@router.delete("/me/api-key")
async def revoke_api_key(
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    إلغاء مفتاح API الحالي
    """
    user = db.query(User).filter(User.id == current_user.get("user_id")).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    user.api_key = None
    db.commit()
    
    logger.info(f"❌ تم إلغاء مفتاح API للمستخدم: {user.username}")
    
    return {
        "message": "تم إلغاء مفتاح API بنجاح",
        "status": "success"
    }

# ============================================
# التحقق من البريد الإلكتروني (سنضيفه لاحقاً)
# ============================================

@router.get("/verify-email/{token}")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """
    التحقق من البريد الإلكتروني
    """
    # سنضيف هذه الوظيفة لاحقاً مع نظام البريد
    return {"message": "سيتم إضافة التحقق من البريد قريباً"}
