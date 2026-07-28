# backend/app/models/alert.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..core.database import Base

class AlertType(str, enum.Enum):
    PRICE = "price"
    VOLUME = "volume"
    TECHNICAL = "technical"
    NEWS = "news"
    EARNINGS = "earnings"

class AlertCondition(str, enum.Enum):
    ABOVE = "above"
    BELOW = "below"
    CROSSES_ABOVE = "crosses_above"
    CROSSES_BELOW = "crosses_below"
    INCREASES_BY = "increases_by"
    DECREASES_BY = "decreases_by"

class AlertStatus(str, enum.Enum):
    ACTIVE = "active"
    TRIGGERED = "triggered"
    DISABLED = "disabled"
    EXPIRED = "expired"

class Alert(Base):
    """نموذج التنبيهات"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    alert_type = Column(Enum(AlertType), nullable=False)
    condition = Column(Enum(AlertCondition), nullable=False)
    threshold = Column(Float, nullable=False)
    
    # For technical alerts
    indicator = Column(String(50), nullable=True)
    timeframe = Column(String(20), nullable=True)
    
    # Trigger information
    triggered_at = Column(DateTime(timezone=True), nullable=True)
    triggered_price = Column(Float, nullable=True)
    trigger_message = Column(String(500), nullable=True)
    
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    is_sent = Column(Boolean, default=False)
    
    # Notification preferences
    notify_email = Column(Boolean, default=True)
    notify_push = Column(Boolean, default=False)
    notify_webhook = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="alerts")
    stock_alerts = relationship("StockAlert", back_populates="alert", cascade="
