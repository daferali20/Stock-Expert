# backend/app/models/news.py
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base

class NewsArticle(Base):
    """أخبار الأسهم"""
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String(500), nullable=False)
    
    # Categories and tags
    category = Column(String(50), nullable=True)
    tags = Column(JSON, default=[])
    sentiment = Column(Float, nullable=True)  # -1 to 1
    
    # Stock mentions
    stock_symbols = Column(JSON, default=[])  # List of stock symbols mentioned
    
    # Dates
    published_at = Column(DateTime(timezone=True), nullable=False)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Quality and engagement
    relevance_score = Column(Float, nullable=True)
    engagement_score = Column(Float, nullable=True)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    user_reads = relationship("UserNewsRead", back_populates="article", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<NewsArticle {self.title[:50]}...>"

class UserNewsRead(Base):
    """تتبع قراءة المستخدم للأخبار"""
    __tablename__ = "user_news_read"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("news_articles.id", ondelete="CASCADE"), nullable=False)
    
    read_at = Column(DateTime(timezone=True), server_default=func.now())
    is_saved = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User")
    article = relationship("NewsArticle", back_populates="user_reads")
    
    def __repr__(self):
        return f"<UserNewsRead User {self.user_id} - Article {self.article_id}>"
