# backend/app/core/security.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
import secrets
import hashlib
import hmac
import re
from functools import wraps

from .config import settings

# ============================================
# Password Hashing
# ============================================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS
)

# ============================================
# Security Schemas
# ============================================
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/oauth2")

# ============================================
# Password Policy
# ============================================
class PasswordPolicy:
    """قواعد كلمة المرور"""
    
    MIN_LENGTH = settings.PASSWORD_MIN_LENGTH
    REQUIRE_UPPER = True
    REQUIRE_LOWER = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = True
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    COMMON_PASSWORDS = [
        "password", "123456", "qwerty", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "hello"
    ]
    
    @classmethod
    def validate(cls, password: str) -> tuple[bool, Optional[str]]:
        """Validate password against policy"""
        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters"
        
        if cls.REQUIRE_UPPER and not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if cls.REQUIRE_LOWER and not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if cls.REQUIRE_DIGIT and not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        if cls.REQUIRE_SPECIAL and not any(c in cls.SPECIAL_CHARS for c in password):
            return False, f"Password must contain at least one special character: {cls.SPECIAL_CHARS}"
        
        if password.lower() in cls.COMMON_PASSWORDS:
            return False, "Password is too common"
        
        return True, None

# ============================================
# JWT Token Service
# ============================================
class TokenService:
    """خدمة التوكنات المتكاملة"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "type": "access",
            "iat": datetime.utcnow()
        })
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({
            "exp": expire,
            "type": "refresh",
            "iat": datetime.utcnow()
        })
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode and validate token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        payload = TokenService.decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Create new tokens
        token_data = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "username": payload.get("username"),
            "role": payload.get("role")
        }
        
        return {
            "access_token": TokenService.create_access_token(token_data),
            "refresh_token": TokenService.create_refresh_token(token_data)
        }

# ============================================
# API Key Service
# ============================================
class APIKeyService:
    """خدمة مفاتيح API"""
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate secure API key"""
        return f"bk_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def verify_api_key(plain_key: str, hashed_key: str) -> bool:
        """Verify API key"""
        return hmac.compare_digest(
            APIKeyService.hash_api_key(plain_key),
            hashed_key
        )

# ============================================
# Rate Limiting
# ============================================
class RateLimiter:
    """محدد معدل الطلبات"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
    
    async def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check if request is allowed"""
        if not self.redis:
            return True  # No rate limiting if redis not available
        
        current = await self.redis.get(key)
        if current is None:
            await self.redis.setex(key, window, 1)
            return True
        
        if int(current) >= limit:
            return False
        
        await self.redis.incr(key)
        return True

# ============================================
# CSRF Protection
# ============================================
class CSRFToken:
    """إدارة توكنات CSRF"""
    
    @staticmethod
    def generate_token() -> str:
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_token(token: str, stored_token: str) -> bool:
        """Validate CSRF token"""
        return hmac.compare_digest(token, stored_token)

# ============================================
# Input Validation
# ============================================
class InputValidator:
    """التحقق من صحة المدخلات"""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """تنظيف المدخلات من الأحرف الخطرة"""
        # Remove potentially dangerous characters
        dangerous = ['<', '>', '&', '"', "'", '/', ';', '=', '(', ')']
        for char in dangerous:
            text = text.replace(char, '')
        return text.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """التحقق من صحة البريد الإلكتروني"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """التحقق من صحة اسم المستخدم"""
        pattern = r'^[a-zA-Z0-9_]{3,50}$'
        return bool(re.match(pattern, username))

# ============================================
# Data Encryption (for sensitive data)
# ============================================
class DataEncryption:
    """تشفير البيانات الحساسة"""
    
    @staticmethod
    def encrypt(data: str) -> str:
        """Encrypt data"""
        # TODO: Implement actual encryption using cryptography library
        # For now, simple base64 encoding
        import base64
        return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def decrypt(encrypted_data: str) -> str:
        """Decrypt data"""
        import base64
        return base64.b64decode(encrypted_data.encode()).decode()

# ============================================
# Security Headers
# ============================================
class SecurityHeaders:
    """إعدادات رؤوس الأمان"""
    
    @staticmethod
    def get_headers() -> Dict[str, str]:
        """Get security headers"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

# ============================================
# Convenience Functions
# ============================================
def hash_password(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from token"""
    try:
        payload = TokenService.decode_token(token)
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "username": payload.get("username"),
            "role": payload.get("role")
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def require_role(roles: List[str]):
    """Decorator to require specific roles"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user or current_user.get('role') not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator
