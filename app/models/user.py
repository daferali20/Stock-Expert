# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    PREMIUM = "premium"
    PRO = "pro"
    ANALYST = "analyst"

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200))
    hashed_password = Column(String(255), nullable=False)
    
    role = Column(Enum(UserRole), default=UserRole.USER)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    subscription_expires_at = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_2fa_enabled = Column(Boolean, default=False)
    _2fa_secret = Column(String(32), nullable=True)
    
    api_key_hash = Column(String(64), nullable=True, unique=True)
    api_key_last_used = Column(DateTime, nullable=True)
    
    preferences = Column(JSON, default={})
    settings = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    watchlists = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
    stock_recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    @property
    def is_premium(self) -> bool:
        return self.subscription_tier in [SubscriptionTier.PREMIUM, SubscriptionTier.PRO]
    
    @property
    def is_pro(self) -> bool:
        return self.subscription_tier == SubscriptionTier.PRO
    
    @property
    def has_active_subscription(self) -> bool:
        if self.subscription_tier == SubscriptionTier.FREE:
            return True
        if not self.subscription_expires_at:
            return False
        return self.subscription_expires_at > func.now()
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
