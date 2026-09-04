"""
SQLAlchemy ORM Models
Defines database schema for personality typing system
"""

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, JSON, Boolean, Text, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

Base = declarative_base()


# ==================== ENUMS ====================

class UserType(str, enum.Enum):
    """User type enumeration"""
    STUDENT = "student"
    EMPLOYEE = "employee"
    ADMIN = "admin"


class SurveyType(str, enum.Enum):
    """Survey type enumeration"""
    STUDENT = "student"
    ENTERPRISE = "enterprise"


class Seniority(str, enum.Enum):
    """Employment seniority levels"""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class SubscriptionTier(str, enum.Enum):
    """Organization subscription tiers"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


# ==================== CORE MODELS ====================

class User(Base):
    """User model - Student or Employee"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    user_type = Column(SQLEnum(UserType), default=UserType.STUDENT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    surveys = relationship("Survey", back_populates="user", cascade="all, delete-orphan")
    profiles = relationship("PersonalityProfile", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.name or self.email}>"


class Organization(Base):
    """Organization model - Companies using the system"""
    __tablename__ = "organizations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=True)
    size = Column(Integer, nullable=True)
    subscription_tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE)
    max_employees = Column(Integer, default=100)
    api_key = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    surveys = relationship("Survey", back_populates="organization", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="organization", cascade="all, delete-orphan")
    teams = relationship("Team", back_populates="organization", cascade="all, delete-orphan")
    job_openings = relationship("JobOpening", back_populates="organization", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Organization {self.name}>"


class Survey(Base):
    """Survey model - Individual survey instances"""
    __tablename__ = "surveys"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    survey_type = Column(SQLEnum(SurveyType), default=SurveyType.STUDENT)
    qr_code_hash = Column(String(255), unique=True, nullable=True)
    qr_url = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    completion_time_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="surveys")
    organization = relationship("Organization", back_populates="surveys")
    responses = relationship("SurveyResponse", back_populates="survey", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Survey {self.id[:8]}... ({self.survey_type})>"


class SurveyResponse(Base):
    """Individual survey response"""
    __tablename__ = "survey_responses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    survey_id = Column(String(36), ForeignKey("surveys.id"), nullable=False)
    question_id = Column(String(50), nullable=False)
    answer_value = Column(Integer, nullable=True)  # 1-5 for Likert
    answer_text = Column(Text, nullable=True)  # For open-ended
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    survey = relationship("Survey", back_populates="responses")
    
    __table_args__ = (
        UniqueConstraint('survey_id', 'question_id', name='uq_survey_question'),
    )
    
    def __repr__(self):
        return f"<SurveyResponse {self.question_id}={self.answer_value}>"


class PersonalityProfile(Base):
    """Calculated personality profile from survey"""
    __tablename__ = "personality_profiles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    survey_id = Column(String(36), ForeignKey("surveys.id"), nullable=True)
    
    # Big Five Scores
    openness = Column(Float, nullable=False)
    conscientiousness = Column(Float, nullable=False)
    extraversion = Column(Float, nullable=False)
    agreeableness = Column(Float, nullable=False)
    emotional_stability = Column(Float, nullable=False)
    
    # Type Classifications
    work_type = Column(String(50), nullable=False)
    work_type_confidence = Column(Float, nullable=False)
    social_type = Column(String(50), nullable=False)
    social_type_confidence = Column(Float, nullable=False)
    
    # Functional Archetypes (JSON array)
    archetypes = Column(JSON)  # [{name, score, reasoning}, ...]
    primary_archetype = Column(String(50), nullable=False)
    
    # NLP Processed Data
    detected_interests = Column(JSON, nullable=True)  # [interest1, interest2, ...]
    work_environment = Column(String(255), nullable=True)
    ideal_teammates = Column(JSON, nullable=True)  # [type1, type2, ...]
    
    # Metadata
    raw_scores = Column(JSON, nullable=True)  # For debugging
    version = Column(Integer, default=1)  # Schema version
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profiles")
    
    def __repr__(self):
        return f"<PersonalityProfile {self.work_type}-{self.social_type}>"


class Employee(Base):
    """Employee in organization"""
    __tablename__ = "employees"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    department = Column(String(100), nullable=True)
    current_role = Column(String(255), nullable=True)
    seniority = Column(SQLEnum(Seniority), default=Seniority.MID)
    profile_id = Column(String(36), ForeignKey("personality_profiles.id"), nullable=True)
    manager_id = Column(String(36), ForeignKey("employees.id"), nullable=True)
    
    # Role Fit Analysis
    role_fit_score = Column(Float, nullable=True)  # 0-1
    fit_analysis = Column(JSON, nullable=True)  # {fit_score, reason, recommendation}
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="employees")
    profile = relationship("PersonalityProfile", foreign_keys=[profile_id])
    manager = relationship("Employee", remote_side=[id], foreign_keys=[manager_id])
    team_memberships = relationship("TeamMember", back_populates="employee", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('org_id', 'email', name='uq_org_employee_email'),
    )
    
    def __repr__(self):
        return f"<Employee {self.name} ({self.current_role})>"


class Team(Base):
    """Team within organization"""
    __tablename__ = "teams"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    department = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    manager_id = Column(String(36), ForeignKey("employees.id"), nullable=True)
    
    # Team Analysis
    personality_diversity_score = Column(Float, nullable=True)  # 0-1
    work_type_balance_score = Column(Float, nullable=True)  # 0-1
    archetype_balance_score = Column(Float, nullable=True)  # 0-1
    team_analysis = Column(JSON, nullable=True)  # Detailed analysis
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="teams")
    manager = relationship("Employee", foreign_keys=[manager_id])
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Team {self.name}>"


class TeamMember(Base):
    """Team membership"""
    __tablename__ = "team_members"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.id"), nullable=False)
    role_in_team = Column(String(100), nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="members")
    employee = relationship("Employee", back_populates="team_memberships")
    
    __table_args__ = (
        UniqueConstraint('team_id', 'employee_id', name='uq_team_employee'),
    )
    
    def __repr__(self):
        return f"<TeamMember {self.employee_id} in {self.team_id}>"


class JobOpening(Base):
    """Job opening to be filled"""
    __tablename__ = "job_openings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    department = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="open")  # open, closed, filled
    
    # Ideal Profile
    ideal_work_type = Column(String(50), nullable=True)
    ideal_social_type = Column(String(50), nullable=True)
    ideal_archetype = Column(String(50), nullable=True)
    ideal_profile = Column(JSON, nullable=True)  # Full ideal profile
    
    seniority_level = Column(SQLEnum(Seniority), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    filled_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="job_openings")
    candidates = relationship("Candidate", back_populates="job_opening", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<JobOpening {self.title}>"


class Candidate(Base):
    """Candidate for job opening"""
    __tablename__ = "candidates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_opening_id = Column(String(36), ForeignKey("job_openings.id"), nullable=False)
    external_id = Column(String(255), nullable=True)  # Internal/External ID
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    
    # Predicted Profile (from CV/LinkedIn)
    predicted_work_type = Column(String(50), nullable=True)
    predicted_social_type = Column(String(50), nullable=True)
    predicted_archetype = Column(String(50), nullable=True)
    prediction_confidence = Column(Float, nullable=True)
    
    # Team Fit
    team_fit_score = Column(Float, nullable=True)  # 0-1
    compatibility_analysis = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(50), default="new")  # new, reviewed, shortlisted, rejected, hired
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_opening = relationship("JobOpening", back_populates="candidates")
    
    def __repr__(self):
        return f"<Candidate {self.name}>"


class Report(Base):
    """Generated report"""
    __tablename__ = "reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(String(36), ForeignKey("personality_profiles.id"), nullable=True)
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=True)
    
    report_type = Column(String(50))  # student, employee, team, organization
    title = Column(String(255), nullable=False)
    content = Column(JSON)  # Report content
    pdf_path = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Report {self.title}>"


class AuditLog(Base):
    """Audit log for tracking changes"""
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))  # User, Survey, Profile, etc.
    entity_id = Column(String(36))
    changes = Column(JSON, nullable=True)
    user_id = Column(String(36), nullable=True)
    ip_address = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AuditLog {self.action} on {self.entity_type}>"
