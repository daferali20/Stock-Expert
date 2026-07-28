# backend/app/core/database.py
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator, Optional
import logging
from contextlib import contextmanager

from .config import settings

logger = logging.getLogger(__name__)

# ============================================
# Database Engine
# ============================================
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DATABASE_ECHO,
    connect_args={
        "connect_timeout": 10,
        "keepalives_idle": 60,
        "keepalives_interval": 10,
        "keepalives_count": 3,
    }
)

# ============================================
# Session Factory
# ============================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()

# ============================================
# Database Events
# ============================================
@event.listens_for(engine, "connect")
def set_pg_settings(dbapi_conn, connection_record):
    """إعدادات PostgreSQL عند الاتصال"""
    with dbapi_conn.cursor() as cursor:
        cursor.execute("SET statement_timeout = '30s'")
        cursor.execute("SET idle_in_transaction_session_timeout = '60s'")
        cursor.execute("SET lock_timeout = '5s'")

# ============================================
# Database Session Management
# ============================================
def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ============================================
# Database Initialization
# ============================================
def init_db():
    """Initialize database"""
    logger.info("Initializing database...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def check_db_connection() -> bool:
    """Check database connection"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

# ============================================
# Database Utilities
# ============================================
async def get_db_stats() -> dict:
    """Get database statistics"""
    try:
        with engine.connect() as conn:
            # Get table sizes
            result = conn.execute(text("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
                LIMIT 10
            """))
            tables = [{"table": r[0] + '.' + r[1], "size": r[2]} for r in result]
            
            # Get connection stats
            result = conn.execute(text("""
                SELECT count(*) as connections,
                       sum(CASE WHEN state = 'idle' THEN 1 ELSE 0 END) as idle,
                       sum(CASE WHEN state = 'active' THEN 1 ELSE 0 END) as active
                FROM pg_stat_activity
                WHERE datname = current_database()
            """))
            stats = result.first()
            
            return {
                "tables": tables,
                "connections": {
                    "total": stats[0],
                    "idle": stats[1],
                    "active": stats[2]
                }
            }
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}
