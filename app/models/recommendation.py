# backend/app/models/recommendation.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ..core.database import Base

class RecommendationAction(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    STRONG_BUY = "strong_buy"
    STRONG_SELL = "strong_sell"

class Recommendation(Base):
    """توصيات الذكاء الاصطناعي"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    # Recommendation
    action = Column(Enum(RecommendationAction), nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0-100
    target_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    
    # Reasoning
    reasoning = Column(Text, nullable=True)
    factors = Column(JSON, default=[])  # List of factors considered
    
    # Technical analysis
    technical_summary = Column(Text, nullable=True)
    technical_indicators = Column(JSON, default={})
    
    # Fundamental analysis
    fundamental_summary = Column(Text, nullable=True)
    fundamental_metrics = Column(JSON, default={})
    
    # Sentiment analysis
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    sentiment_summary = Column(Text, nullable=True)
    
    # Performance tracking
    actual_return = Column(Float, nullable=True)
    is_executed = Column(Boolean, default=False)
    executed_price = Column(Float, nullable=True)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Validity
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="stock_recommendations")
    stock = relationship("Stock", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation {self.stock.symbol} - {self.action}>"
