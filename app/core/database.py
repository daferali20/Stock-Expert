# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
import logging

from .config import settings

# إعداد السجلات
logger = logging.getLogger(__name__)

# إنشاء محرك قاعدة البيانات مع إعدادات احترافية
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # التحقق من صحة الاتصال قبل الاستخدام
    pool_recycle=3600,   # إعادة تدوير الاتصالات كل ساعة
    echo=settings.DEBUG, # تسجيل استعلامات SQL في وضع التطوير
)

# مصنع جلسات قاعدة البيانات
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# الفئة الأساسية للنماذج
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    دالة للحصول على جلسة قاعدة البيانات.
    تستخدم كـ Dependency في FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    تهيئة قاعدة البيانات - إنشاء الجداول
    """
    logger.info("جاري تهيئة قاعدة البيانات...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        logger.error(f"خطأ في تهيئة قاعدة البيانات: {e}")
        raise

def check_db_connection() -> bool:
    """
    التحقق من صحة اتصال قاعدة البيانات
    """
    try:
        with SessionLocal() as session:
            session.execute("SELECT 1")
        logger.info("اتصال قاعدة البيانات يعمل بشكل صحيح")
        return True
    except Exception as e:
        logger.error(f"فشل الاتصال بقاعدة البيانات: {e}")
        return False
