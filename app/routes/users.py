# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import Optional, List

from ..core.database import get_db
from ..core.security import security_service
from ..models.user import User, UserRole
from ..schemas.user import UserResponse, UserRoleEnum

router = APIRouter()

# ============================================
# مسارات إدارة المستخدمين (للمشرفين فقط)
# ============================================

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[UserRoleEnum] = None,
    is_active: Optional[bool] = None,
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    الحصول على قائمة المستخدمين (للمشرفين فقط)
    """
    # التحقق من صلاحية المشرف
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية الوصول إلى هذه البيانات"
        )
    
    query = db.query(User)
    
    # فلترة البحث
    if search:
        query = query.filter(
            or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.full_name.ilike(f"%{search}%")
            )
        )
    
    # فلترة حسب الدور
    if role:
        query = query.filter(User.role == role)
    
    # فلترة حسب النشاط
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # ترتيب حسب تاريخ الإنشاء
    query = query.order_by(desc(User.created_at))
    
    # تطبيق التقسيم
    users = query.offset(skip).limit(limit).all()
    
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    الحصول على معلومات مستخدم محدد (للمشرفين فقط)
    """
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية الوصول إلى هذه البيانات"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_admin(
    user_id: int,
    user_data: dict,
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    تحديث بيانات مستخدم (للمشرفين فقط)
    """
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية تنفيذ هذا الإجراء"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    # تحديث الحقول المسموح بها
    allowed_fields = ["full_name", "email", "role", "is_active", "is_verified"]
    
    for field in allowed_fields:
        if field in user_data:
            # التحقق من صحة الدور
            if field == "role" and user_data[field]:
                try:
                    user.role = UserRole(user_data[field])
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="دور غير صالح"
                    )
            else:
                setattr(user, field, user_data[field])
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    حذف مستخدم (للمشرفين فقط)
    """
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية تنفيذ هذا الإجراء"
        )
    
    # منع حذف النفس
    if user_id == int(current_user.get("user_id")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="لا يمكنك حذف حسابك الخاص من هنا"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    db.delete(user)
    db.commit()
    
    return {
        "message": f"تم حذف المستخدم {user.username} بنجاح",
        "status": "success"
    }

@router.post("/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    تفعيل حساب مستخدم (للمشرفين فقط)
    """
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية تنفيذ هذا الإجراء"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    user.is_active = True
    db.commit()
    
    return {
        "message": f"تم تفعيل حساب {user.username} بنجاح",
        "status": "success"
    }

@router.post("/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    current_user: dict = Depends(security_service.get_current_user),
    db: Session = Depends(get_db)
):
    """
    تعطيل حساب مستخدم (للمشرفين فقط)
    """
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية تنفيذ هذا الإجراء"
        )
    
    # منع تعطيل النفس
    if user_id == int(current_user.get("user_id")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="لا يمكنك تعطيل حسابك الخاص"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستخدم غير موجود"
        )
    
    user.is_active = False
    db.commit()
    
    return {
        "message": f"تم تعطيل حساب {user.username} بنجاح",
        "status": "success"
    }
