# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..core.database import Base

class UserRole(str, enum.Enum):
    """
    أدوار المستخدمين
    """
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"
    ANALYST = "analyst"

class User(Base):
    """
    نموذج المستخدم في قاعدة البيانات
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200))
    hashed_password = Column(String(255), nullable=False)
    
    # معلومات المستخدم
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # التوكنات
    api_key = Column(String(255), nullable=True, unique=True)
    
    # الطوابع الزمنية
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # العلاقات (سنضيفها لاحقاً)
    # portfolios = relationship("Portfolio", back_populates="user")
    # watchlists = relationship("Watchlist", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    @property
    def is_premium(self) -> bool:
        return self.role in [UserRole.PREMIUM, UserRole.ADMIN]
