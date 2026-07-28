# /mount/src/stock-expert/app/api/auth.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ============================================
# نماذج البيانات
# ============================================
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool = True

# ============================================
# مسارات API
# ============================================
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """تسجيل مستخدم جديد"""
    # محاكاة التسجيل
    user_id = str(uuid.uuid4())
    return UserResponse(
        id=user_id,
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name
    )

@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    """تسجيل الدخول"""
    # محاكاة تسجيل الدخول
    if login_data.email and login_data.password:
        return TokenResponse(
            access_token="mock_access_token_" + str(uuid.uuid4()),
            refresh_token="mock_refresh_token_" + str(uuid.uuid4())
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """الحصول على معلومات المستخدم الحالي"""
    return UserResponse(
        id="1",
        email="user@example.com",
        username="testuser",
        full_name="Test User"
    )
