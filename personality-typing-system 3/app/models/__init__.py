"""
Models Package
Core personality models and ML engines
"""

try:
    from .personality import PersonalityTyping, BigFiveScores, PersonalityProfile
except ImportError:
    PersonalityTyping = None
    BigFiveScores = None
    PersonalityProfile = None

try:
    from .archetype import ArchetypeCalculator, ArchetypeAnalysis
except ImportError:
    ArchetypeCalculator = None
    ArchetypeAnalysis = None

try:
    from .job_recommendations import JobRecommendationEngine, Job
except ImportError:
    JobRecommendationEngine = None
    Job = None

try:
    from .team_compatibility import TeamCompatibilityEngine, TeamMember
except ImportError:
    TeamCompatibilityEngine = None
    TeamMember = None

try:
    from .role_prediction import RoleFitPredictionEngine, Role
except ImportError:
    RoleFitPredictionEngine = None
    Role = None

__all__ = [
    # Personality Models
    "PersonalityTyping",
    "BigFiveScores",
    "PersonalityProfile",
    
    # Archetype Models
    "ArchetypeCalculator",
    "ArchetypeAnalysis",
    
    # ML Engines
    "JobRecommendationEngine",
    "Job",
    "TeamCompatibilityEngine",
    "TeamMember",
    "RoleFitPredictionEngine",
    "Role",
]
