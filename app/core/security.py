# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import hashlib
import hmac

from .config import settings

# إعدادات التشفير
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # عدد جولات التشفير
)

# مصادقة التوكن
security = HTTPBearer()

class SecurityService:
    """
    خدمة الأمان المتكاملة
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        تشفير كلمة المرور باستخدام bcrypt
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        التحقق من صحة كلمة المرور
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        إنشاء توكن وصول JWT
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """
        إنشاء توكن تحديث (Refresh Token) طويل الأجل
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        فك تشفير التوكن والتحقق من صحته
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="توكن غير صالح أو منتهي الصلاحية",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def get_current_user(token: str = Depends(security)):
        """
        الحصول على المستخدم الحالي من التوكن
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="لم يتم التحقق من الهوية",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = SecurityService.decode_token(token.credentials)
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            return {"user_id": user_id, "email": payload.get("email")}
        except JWTError:
            raise credentials_exception
    
    @staticmethod
    def generate_api_key() -> str:
        """
        إنشاء مفتاح API عشوائي وآمن
        """
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """
        تشفير مفتاح API للتخزين الآمن
        """
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def verify_api_key(plain_key: str, hashed_key: str) -> bool:
        """
        التحقق من صحة مفتاح API
        """
        return hmac.compare_digest(
            SecurityService.hash_api_key(plain_key),
            hashed_key
        )

# توكن للاستخدام المباشر
security_service = SecurityService()

# دالة مساعدة للتحقق من التوكن في المسارات
async def get_current_user_id(current_user: dict = Depends(security_service.get_current_user)):
    """
    الحصول على ID المستخدم الحالي
    """
    return current_user.get("user_id")
