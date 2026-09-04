"""
Database Connection Management
Handles database connection and session creation
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging
from typing import Generator
from app.config import settings

logger = logging.getLogger(__name__)

# ==================== ENGINE CREATION ====================

def create_db_engine():
    """Create database engine based on configuration"""
    
    database_url = settings.get_database_url()
    
    # SQLite configuration
    if settings.DB_TYPE == "sqlite":
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=settings.DB_ECHO
        )
        
        # Enable foreign keys for SQLite
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    
    # PostgreSQL configuration
    elif settings.DB_TYPE == "postgresql":
        engine = create_engine(
            database_url,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            echo=settings.DB_ECHO,
            pool_pre_ping=True  # Test connections before using
        )
    
    else:
        raise ValueError(f"Unsupported database type: {settings.DB_TYPE}")
    
    logger.info(f"Database engine created: {settings.DB_TYPE}")
    return engine


# ==================== SESSION MANAGEMENT ====================

# Create engine
engine = create_db_engine()

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session
    Usage in Streamlit:
        db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    """Get new database session"""
    return SessionLocal()


# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """Initialize database schema"""
    from app.database.models import Base
    
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema created successfully")


def drop_all_tables():
    """Drop all tables (dangerous - use only for testing)"""
    from app.database.models import Base
    
    logger.warning("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.warning("All tables dropped")


def reset_db():
    """Reset database (drop + recreate)"""
    drop_all_tables()
    init_db()
    logger.info("Database reset complete")


# ==================== HEALTH CHECKS ====================

def check_db_connection() -> bool:
    """Check if database is accessible"""
    try:
        db = get_session()
        db.execute("SELECT 1")
        db.close()
        logger.info("Database connection OK")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def get_db_status() -> dict:
    """Get database status information"""
    try:
        db = get_session()
        
        # Get table count
        from app.database.models import Base
        tables = len(Base.metadata.tables)
        
        # Test connection
        db.execute("SELECT 1")
        
        db.close()
        
        return {
            "status": "healthy",
            "type": settings.DB_TYPE,
            "tables": tables,
            "connected": True
        }
    except Exception as e:
        return {
            "status": "error",
            "type": settings.DB_TYPE,
            "error": str(e),
            "connected": False
        }


# ==================== CONTEXT MANAGERS ====================

class DatabaseSession:
    """Context manager for database sessions"""
    
    def __init__(self):
        self.session = None
    
    def __enter__(self) -> Session:
        self.session = get_session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()


# ==================== INITIALIZATION ====================

if __name__ == "__main__":
    # Initialize database if run directly
    init_db()
    print("Database initialized successfully")
