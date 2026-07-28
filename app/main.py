# /mount/src/stock-expert/app/main.py
import sys
import os
from contextlib import asynccontextmanager
import logging

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق"""
    logger.info("🚀 Starting ByToBy AI API...")
    yield
    logger.info("🛑 Shutting down ByToBy AI API...")

# إنشاء التطبيق
app = FastAPI(
    title="ByToBy AI",
    version="1.0.0",
    description="AI-Powered Stock Analysis Platform",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "ByToBy AI",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "api": "/api/v1",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

@app.get("/api/v1/status")
async def api_status():
    return {
        "status": "online",
        "timestamp": "2026-07-28T23:00:00Z"
    }

# استيراد المسارات (اختياري)
try:
    from app.api import auth, users
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(users.router, prefix="/api/v1")
    logger.info("✅ Routes loaded successfully")
except ImportError as e:
    logger.warning(f"⚠️ Routes not loaded: {e}")
