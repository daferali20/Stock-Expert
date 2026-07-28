# backend/app/models/watchlist.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base

class Watchlist(Base):
    """قائمة مراقبة الأسهم"""
    __tablename__ = "watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    is_default = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    
    # Settings
    settings = Column(JSON, default={})  # e.g., alerts, notifications
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="watchlists")
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Watchlist {self.name} - User {self.user_id}>"

class WatchlistItem(Base):
    """عنصر في قائمة المراقبة"""
    __tablename__ = "watchlist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    watchlist_id = Column(Integer, ForeignKey("watchlists.id", ondelete="CASCADE"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"), nullable=False)
    
    # Notes and custom data
    notes = Column(String(500), nullable=True)
    alert_price = Column(Float, nullable=True)
    alert_triggered = Column(Boolean, default=False)
    
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    watchlist = relationship("Watchlist", back_populates="items")
    stock = relationship("Stock", back_populates="watchlist_items")
    
    def __repr__(self):
        return f"<WatchlistItem {self.stock.symbol} in {self.watchlist.name}>"
