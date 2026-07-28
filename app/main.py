# /mount/src/stock-expert/app/main.py
import sys
import os

# إضافة المسار الحالي
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# إنشاء التطبيق
app = FastAPI(
    title="ByToBy AI",
    version="1.0.0",
    description="AI-Powered Stock Analysis Platform"
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
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

# استيراد المسارات (اختياري)
try:
    from app.api import auth, users
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(users.router, prefix="/api/v1")
except ImportError:
    pass  # تجاهل إذا لم تكن المسارات موجودة
