"""
Configuration Management
Zentrale Konfiguration für alle App-Settings
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

# Load environment variables
load_dotenv()

# Directories
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

# Create directories if not exist
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


class Settings:
    """Central Settings Class"""
    
    # ==================== APP SETTINGS ====================
    APP_NAME: str = "Personality Typing System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    APP_ENV: str = os.getenv("APP_ENV", "development")  # development, staging, production
    
    # ==================== STREAMLIT SPECIFIC ====================
    STREAMLIT_CONFIG = {
        "page_icon": "🧠",
        "layout": "wide",
        "initial_sidebar_state": "expanded",
        "theme": {
            "primaryColor": "#0066ff",
            "backgroundColor": "#ffffff",
            "secondaryBackgroundColor": "#f0f2f6",
            "textColor": "#262730",
            "font": "sans serif"
        }
    }
    
    # ==================== DATABASE SETTINGS ====================
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./personality_system.db"
    )
    
    # SQLite fallback
    if "sqlite" in DATABASE_URL:
        DB_TYPE = "sqlite"
    elif "postgresql" in DATABASE_URL:
        DB_TYPE = "postgresql"
    else:
        DB_TYPE = "unknown"
    
    # Database connection pooling (nur für production DB)
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "40"))
    DB_ECHO: bool = DEBUG  # Print SQL queries in debug mode
    
    # ==================== SURVEY SETTINGS ====================
    SURVEY_TIMEOUT_MINUTES: int = 30
    MAX_RESPONDENTS_PER_ORG: int = 1000
    QR_CODE_EXPIRY_DAYS: int = 30
    
    # Survey Item Counts
    STUDENT_WORK_TYPE_ITEMS: int = 18  # Big Five
    STUDENT_INTERESTS_ITEMS: int = 4   # Open-ended
    ENTERPRISE_WORK_TYPE_ITEMS: int = 18
    ENTERPRISE_SKILLS_ITEMS: int = 10
    ENTERPRISE_TEAM_ITEMS: int = 7
    
    # ==================== SCORING & THRESHOLDS ====================
    TYPE_CONFIDENCE_THRESHOLD: float = 0.65
    ARCHETYPE_ALIGNMENT_THRESHOLD: float = 0.60
    TEAM_COMPATIBILITY_THRESHOLD: float = 0.60
    ROLE_FIT_GOOD: float = 0.75
    ROLE_FIT_ACCEPTABLE: float = 0.60
    
    # Archetype Weights
    SLOP_CANNON_BONUS = {
        "E": 0.20,
        "O": 0.15,
        "C": -0.15
    }
    
    STITCHER_BONUS = {
        "C": 0.25,
        "O": 0.10,
        "A": 0.05
    }
    
    HOT_PERSON_BONUS = {
        "E": 0.25,
        "A": 0.20,
        "ES": 0.10
    }
    
    GROWN_UP_BONUS = {
        "C": 0.20,
        "ES": 0.15,
        "O": 0.05
    }
    
    # ==================== REPORT SETTINGS ====================
    ENABLE_PDF_EXPORT: bool = True
    ENABLE_EXCEL_EXPORT: bool = True
    PDF_MARGIN_MM: int = 10
    PDF_FONT_SIZE: int = 11
    
    # ==================== EMAIL SETTINGS ====================
    ENABLE_EMAIL: bool = os.getenv("ENABLE_EMAIL", "False").lower() == "true"
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "noreply@personality-typing.com")
    SENDER_PASSWORD: str = os.getenv("SENDER_PASSWORD", "")
    EMAIL_FROM_NAME: str = "Personality Typing System"
    
    # Email templates
    STUDENT_EMAIL_SUBJECT: str = "Dein Personality Assessment ist bereit! 🧠"
    EMPLOYEE_EMAIL_SUBJECT: str = "Team Personality Assessment - Bitte ausfüllen 🏢"
    
    # ==================== QR CODE SETTINGS ====================
    QR_CODE_SIZE: int = 300  # pixels
    QR_CODE_FORMAT: str = "png"
    INCLUDE_LOGO_IN_QR: bool = False
    
    # ==================== NLP SETTINGS ====================
    ENABLE_NLP_ANALYSIS: bool = os.getenv("ENABLE_NLP", "True").lower() == "true"
    NLTK_DATA_PATH: str = str(LOGS_DIR / "nltk_data")
    
    # ==================== API KEYS (Future) ====================
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # ==================== LOGGING ====================
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = str(LOGS_DIR / "app.log")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ==================== SECURITY ====================
    SECURE_COOKIES: bool = APP_ENV == "production"
    CORS_ORIGINS: list = ["*"]  # Restrict in production
    
    # ==================== CACHE SETTINGS ====================
    ENABLE_CACHING: bool = True
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    
    # ==================== RATE LIMITING ====================
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    
    # ==================== VALIDATION ====================
    MIN_SURVEY_ANSWERS: int = 15  # Minimum required answers
    ALLOW_INCOMPLETE_SURVEYS: bool = False
    
    # ==================== REPORTING ====================
    STUDENT_REPORT_SECTIONS = [
        "personality_profile",
        "work_type",
        "social_type",
        "functional_archetype",
        "career_recommendations",
        "industry_analysis",
        "skill_gaps",
        "development_plan",
        "ideal_teammates"
    ]
    
    ENTERPRISE_REPORT_SECTIONS = [
        "individual_role_fit",
        "team_analysis",
        "team_compatibility",
        "archetype_distribution",
        "recruitment_gaps",
        "organizational_health",
        "performance_prediction",
        "talent_development"
    ]
    
    # ==================== FEATURE FLAGS ====================
    ENABLE_STUDENT_MODE: bool = True
    ENABLE_ENTERPRISE_MODE: bool = True
    ENABLE_ADMIN_DASHBOARD: bool = True
    ENABLE_API_ENDPOINTS: bool = False  # Beta
    ENABLE_ANALYTICS: bool = True
    
    # ==================== TYPE DEFINITIONS ====================
    WORK_TYPES = [
        "DENKER",
        "ANALYTIKER",
        "UMSETZER",
        "ORGANISATEUR",
        "VERKÄUFER"
    ]
    
    SOCIAL_TYPES = [
        "MODERATOR",
        "INDIVIDUALIST",
        "PARTNER",
        "BEOBACHTER"
    ]
    
    FUNCTIONAL_ARCHETYPES = [
        "SLOP_CANNON",
        "STITCHER",
        "HOT_PERSON",
        "GROWN_UP"
    ]
    
    # ==================== PAGINATION ====================
    ITEMS_PER_PAGE: int = 20
    MAX_ITEMS_PER_PAGE: int = 100
    
    # ==================== BACKUP & EXPORT ====================
    ENABLE_BACKUPS: bool = True
    BACKUP_RETENTION_DAYS: int = 30
    EXPORT_FORMAT_DEFAULT: str = "pdf"  # pdf, excel, json
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the database URL with proper handling"""
        if cls.DB_TYPE == "sqlite":
            # Ensure directory exists for SQLite
            db_path = Path(cls.DATABASE_URL.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        return cls.DATABASE_URL
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production"""
        return cls.APP_ENV == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development"""
        return cls.APP_ENV == "development"


# Export settings instance
settings = Settings()

# Convenience functions
def get_settings() -> Settings:
    """Get settings instance"""
    return settings


def is_production() -> bool:
    """Check if production"""
    return settings.is_production()


def is_development() -> bool:
    """Check if development"""
    return settings.is_development()
