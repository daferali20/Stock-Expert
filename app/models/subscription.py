# backend/app/models/subscription.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..core.database import Base

class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"

class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CRYPTO = "crypto"
    BANK_TRANSFER = "bank_transfer"

class SubscriptionPlan(Base):
    """خطة الاشتراك"""
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    tier = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Pricing
    price_monthly = Column(Float, nullable=True)
    price_yearly = Column(Float, nullable=True)
    currency = Column(String(3), default="USD")
    
    # Features
    features = Column(JSON, default=[])  # List of features
    limits = Column(JSON, default={})    # Usage limits
    
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<SubscriptionPlan {self.name}>"

class UserSubscription(Base):
    """اشتراك المستخدم"""
    __tablename__ = "user_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    
    # Subscription details
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.PENDING)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    
    # Dates
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=False)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Payment details
    amount_paid = Column(Float, nullable=True)
    currency = Column(String(3), default="USD")
    payment_id = Column(String(200), nullable=True)
    
    # Auto-renewal
    auto_renew = Column(Boolean, default=True)
    last_renewal = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    plan = relationship("SubscriptionPlan")
    payment_history = relationship("PaymentHistory", back_populates="subscription", cascade="all, delete-orphan")
    
    @property
    def is_active(self) -> bool:
        if self.status != SubscriptionStatus.ACTIVE:
            return False
        if self.end_date and self.end_date < func.now():
            return False
        return True
    
    def __repr__(self):
        return f"<UserSubscription {self.user_id} - {self.plan.name}>"

class PaymentHistory(Base):
    """سجل المدفوعات"""
    __tablename__ = "payment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("user_subscriptions.id", ondelete="CASCADE"), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_id = Column(String(200), nullable=True)
    status = Column(String(50), default="completed")
    
    # Additional info
    invoice_url = Column(String(500), nullable=True)
    receipt_url = Column(String(500), nullable=True)
    metadata = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    subscription = relationship("UserSubscription", back_populates="payment_history")
    
    def __repr__(self):
        return f"<PaymentHistory {self.id} - ${self.amount}>"
