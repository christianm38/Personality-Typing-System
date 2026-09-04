"""
Personality Typing System
A comprehensive personality assessment and organizational optimization platform
"""

__version__ = "1.0.0"
__author__ = "Christian M (@christianm38)"
__license__ = "MIT"

from app.config import settings, get_settings
from app.database.connection import engine, SessionLocal, get_db, init_db

__all__ = [
    "settings",
    "get_settings",
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
]
