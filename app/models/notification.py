# backend/app/models/notification.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..core.database import Base

class NotificationType(str, enum.Enum):
    PRICE_ALERT = "price_alert"
    NEWS = "news"
    SYSTEM = "system"
    MARKET = "market"
    SUBSCRIPTION = "subscription"
    AI_RECOMMENDATION = "ai_recommendation"
    EARNINGS = "earnings"
    DIVIDEND = "dividend"

class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    PUSH = "push"
    WEBHOOK = "webhook"
    SMS = "sms"
    IN_APP = "in_app"

class Notification(Base):
    """نموذج الإشعارات"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    type = Column(Enum(NotificationType), nullable=False)
    channel = Column(Enum(NotificationChannel), default=NotificationChannel.IN_APP)
    
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    data = Column(JSON, default={})
    
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.id} - {self.type}>"

class NotificationPreference(Base):
    """تفضيلات الإشعارات للمستخدم"""
    __tablename__ = "notification_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Enable/disable different notification types
    price_alerts = Column(Boolean, default=True)
    news_alerts = Column(Boolean, default=True)
    system_alerts = Column(Boolean, default=True)
    market_alerts = Column(Boolean, default=True)
    subscription_alerts = Column(Boolean, default=True)
    ai_recommendations = Column(Boolean, default=True)
    earnings_alerts = Column(Boolean, default=True)
    
    # Channel preferences
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=False)
    
    # Settings
    quiet_hours_start = Column(String(5), nullable=True)  # HH:MM
    quiet_hours_end = Column(String(5), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<NotificationPreference User {self.user_id}>"
