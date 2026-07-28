# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"
    ANALYST = "analyst"

# نماذج الطلبات (Requests)
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8)
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('يجب أن يحتوي اسم المستخدم على أحرف وأرقام فقط')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('يجب أن تحتوي كلمة المرور على رقم على الأقل')
        if not any(char.isupper() for char in v):
            raise ValueError('يجب أن تحتوي كلمة المرور على حرف كبير على الأقل')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRoleEnum] = None

# نماذج الردود (Responses)
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    role: UserRoleEnum
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class ApiKeyResponse(BaseModel):
    api_key: str
    message: str
