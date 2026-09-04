"""Initialize Database with SQLAlchemy Models"""
from app.database.connection import engine
from app.database.models import Base

def init_db():
    """Create all database tables"""
    print("🔧 Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    print("📊 Tables created:")
    print("   - users")
    print("   - organizations")
    print("   - surveys")
    print("   - survey_responses")
    print("   - personality_profiles")
    print("   - employees")
    print("   - teams")
    print("   - team_members")

if __name__ == "__main__":
    init_db()
