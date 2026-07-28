# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .core.config import settings
from .core.database import init_db, check_db_connection
# app.py (Streamlit)
import streamlit as st

st.set_page_config(
    page_title="ByToBy AI",
    page_icon="📈",
    layout="wide"
)

st.title("📈 ByToBy AI - Stock Analysis Platform")
st.write("منصة تحليل الأسهم بالذكاء الاصطناعي")

# يمكنك هنا استدعاء API الخاص بك
# إعداد السجلات
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    إدارة دورة حياة التطبيق
    """
    # بدء التشغيل
    logger.info("🚀 جاري بدء تشغيل ByToBy AI API...")
    
    # التحقق من اتصال قاعدة البيانات
    if not check_db_connection():
        logger.error("❌ فشل الاتصال بقاعدة البيانات")
        raise RuntimeError("لا يمكن بدء التطبيق بدون اتصال بقاعدة البيانات")
    
    # تهيئة قاعدة البيانات
    init_db()
    
    logger.info(f"✅ تم بدء التطبيق بنجاح في وضع {settings.ENVIRONMENT}")
    
    yield
    
    # إيقاف التشغيل
    logger.info("🛑 جاري إيقاف تشغيل التطبيق...")

# إنشاء التطبيق
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Artificial Intelligence Stock Analysis Platform",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# استيراد المسارات
from .routes import auth, users

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# نقاط النهاية الأساسية
@app.get("/")
async def home():
    return {
        "application": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
async def health():
    db_status = check_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "environment": settings.ENVIRONMENT
    }
