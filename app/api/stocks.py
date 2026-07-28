# backend/app/api/stocks.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta

from ..core.database import get_db
from ..core.security import get_current_user
from ..models.stock import Stock, StockHistory
from ..services.polygon_service import PolygonService
from ..services.finnhub_service import FinnhubService

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/search")
async def search_stocks(
    query: str,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search for stocks"""
    stocks = db.query(Stock).filter(
        Stock.symbol.ilike(f"%{query}%") | 
        Stock.name.ilike(f"%{query}%")
    ).limit(limit).all()
    
    return stocks

@router.get("/{symbol}")
async def get_stock_details(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Get detailed stock information"""
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.get("/{symbol}/history")
async def get_stock_history(
    symbol: str,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get stock historical data"""
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    history = db.query(StockHistory).filter(
        StockHistory.stock_id == stock.id,
        StockHistory.date >= cutoff_date
    ).order_by(StockHistory.date).all()
    
    return history
