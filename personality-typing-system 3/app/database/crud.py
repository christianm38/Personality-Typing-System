"""CRUD operations for database models"""
from sqlalchemy.orm import Session
from app.database.models import Survey, PersonalityProfile, User, Organization
from datetime import datetime, timedelta
import uuid
from typing import List, Optional


class SurveyCRUD:
    """CRUD operations for surveys"""
    
    @staticmethod
    def create_survey(
        db: Session, 
        survey_type: str, 
        user_id: str = None, 
        org_id: str = None
    ) -> Survey:
        """
        Create a new survey
        
        Args:
            db: Database session
            survey_type: 'student' or 'enterprise'
            user_id: Optional user ID
            org_id: Optional organization ID
            
        Returns:
            Survey: Created survey object
        """
        survey = Survey(
            id=str(uuid.uuid4()),
            user_id=user_id,
            org_id=org_id,
            survey_type=survey_type,
            qr_code_hash=str(uuid.uuid4()),
            is_completed=False,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.add(survey)
        db.commit()
        db.refresh(survey)
        return survey
    
    @staticmethod
    def get_survey(db: Session, survey_id: str) -> Optional[Survey]:
        """Get survey by ID"""
        return db.query(Survey).filter(Survey.id == survey_id).first()
    
    @staticmethod
    def get_survey_by_qr_hash(db: Session, qr_hash: str) -> Optional[Survey]:
        """Get survey by QR code hash"""
        return db.query(Survey).filter(Survey.qr_code_hash == qr_hash).first()
    
    @staticmethod
    def mark_survey_complete(db: Session, survey_id: str) -> Optional[Survey]:
        """Mark survey as complete"""
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        if survey:
            survey.is_completed = True
            db.commit()
            db.refresh(survey)
        return survey
    
    @staticmethod
    def create_bulk_surveys(
        db: Session, 
        count: int, 
        survey_type: str, 
        org_id: str = None
    ) -> List[Survey]:
        """
        Create multiple surveys for bulk distribution
        
        Args:
            db: Database session
            count: Number of surveys to create
            survey_type: Type of survey
            org_id: Optional organization ID
            
        Returns:
            List[Survey]: Created surveys
        """
        surveys = []
        for _ in range(count):
            survey = SurveyCRUD.create_survey(db, survey_type, org_id=org_id)
            surveys.append(survey)
        return surveys
    
    @staticmethod
    def get_all_surveys(db: Session, limit: int = 100) -> List[Survey]:
        """Get all surveys with limit"""
        return db.query(Survey).limit(limit).all()
    
    @staticmethod
    def get_completed_surveys(db: Session) -> List[Survey]:
        """Get all completed surveys"""
        return db.query(Survey).filter(Survey.is_completed == True).all()
    
    @staticmethod
    def get_pending_surveys(db: Session) -> List[Survey]:
        """Get all pending surveys"""
        return db.query(Survey).filter(Survey.is_completed == False).all()


class PersonalityProfileCRUD:
    """CRUD operations for personality profiles"""
    
    @staticmethod
    def create_profile(
        db: Session,
        survey_id: str,
        scores: dict,
        work_type: str,
        social_type: str = None,
        archetype: str = None,
        user_id: str = None
    ) -> PersonalityProfile:
        """
        Create personality profile from survey responses
        
        Args:
            db: Database session
            survey_id: Survey ID
            scores: Dictionary with Big Five scores (O, C, E, A, ES)
            work_type: Work type classification
            social_type: Social type classification (optional)
            archetype: Functional archetype (optional)
            user_id: User ID (optional)
            
        Returns:
            PersonalityProfile: Created profile
        """
        profile = PersonalityProfile(
            id=str(uuid.uuid4()),
            user_id=user_id,
            survey_id=survey_id,
            openness=scores.get('O', 0),
            conscientiousness=scores.get('C', 0),
            extraversion=scores.get('E', 0),
            agreeableness=scores.get('A', 0),
            emotional_stability=scores.get('ES', 0),
            work_type=work_type,
            work_type_confidence=scores.get('work_type_confidence', 0.65),
            social_type=social_type,
            social_type_confidence=scores.get('social_type_confidence', 0.65),
            primary_archetype=archetype,
            created_at=datetime.utcnow()
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    
    @staticmethod
    def get_profile_by_survey(db: Session, survey_id: str) -> Optional[PersonalityProfile]:
        """Get profile by survey ID"""
        return db.query(PersonalityProfile).filter(
            PersonalityProfile.survey_id == survey_id
        ).first()
    
    @staticmethod
    def get_profile_by_user(db: Session, user_id: str) -> Optional[PersonalityProfile]:
        """Get latest profile by user ID"""
        return db.query(PersonalityProfile).filter(
            PersonalityProfile.user_id == user_id
        ).order_by(PersonalityProfile.created_at.desc()).first()
    
    @staticmethod
    def get_all_profiles(db: Session, limit: int = 100) -> List[PersonalityProfile]:
        """Get all profiles with limit"""
        return db.query(PersonalityProfile).limit(limit).all()


class UserCRUD:
    """CRUD operations for users"""
    
    @staticmethod
    def create_user(
        db: Session,
        name: str,
        email: str,
        user_type: str = "student"
    ) -> User:
        """Create a new user"""
        user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            user_type=user_type,
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()


class OrganizationCRUD:
    """CRUD operations for organizations"""
    
    @staticmethod
    def create_organization(
        db: Session,
        name: str,
        industry: str = None,
        size: int = None
    ) -> Organization:
        """Create a new organization"""
        org = Organization(
            id=str(uuid.uuid4()),
            name=name,
            industry=industry,
            size=size,
            subscription_tier="free",
            created_at=datetime.utcnow()
        )
        db.add(org)
        db.commit()
        db.refresh(org)
        return org
    
    @staticmethod
    def get_organization(db: Session, org_id: str) -> Optional[Organization]:
        """Get organization by ID"""
        return db.query(Organization).filter(Organization.id == org_id).first()
