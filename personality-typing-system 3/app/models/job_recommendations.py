"""
Job Recommendations Engine
Machine Learning-based job matching and recommendations
Uses cosine similarity and profile matching
"""

from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass
import logging

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class Job:
    """Job profile for matching"""
    id: str
    title: str
    industry: str
    description: str
    ideal_work_type: str
    ideal_social_type: str
    ideal_archetype: str
    salary_range: Tuple[int, int]
    growth_potential: float  # 0-1
    work_life_balance: float  # 0-1
    remote_friendly: bool
    team_size: str  # small, medium, large
    required_skills: List[str]
    big_five_profile: Dict[str, float]  # Expected Big Five scores
    difficulty_level: str  # entry, mid, senior, lead


class JobRecommendationEngine:
    """
    ML-powered job recommendation system
    Matches personality profiles to job opportunities
    """
    
    # ==================== JOB DATABASE ====================
    
    JOB_DATABASE: List[Job] = [
        # Tech & Innovation
        Job(
            id="job_001",
            title="Product Engineer",
            industry="Technology",
            description="Build innovative products using latest tech",
            ideal_work_type="DENKER",
            ideal_social_type="INDIVIDUALIST",
            ideal_archetype="SLOP_CANNON",
            salary_range=(80000, 150000),
            growth_potential=0.9,
            work_life_balance=0.6,
            remote_friendly=True,
            team_size="small",
            required_skills=["coding", "product thinking", "creativity"],
            big_five_profile={"O": 4.5, "C": 3.0, "E": 4.0, "A": 3.0, "ES": 4.0},
            difficulty_level="mid"
        ),
        
        Job(
            id="job_002",
            title="Data Scientist",
            industry="Technology",
            description="Analyze data and build predictive models",
            ideal_work_type="ANALYTIKER",
            ideal_social_type="BEOBACHTER",
            ideal_archetype="STITCHER",
            salary_range=(90000, 160000),
            growth_potential=0.85,
            work_life_balance=0.7,
            remote_friendly=True,
            team_size="small",
            required_skills=["statistics", "python", "ML", "analysis"],
            big_five_profile={"O": 4.0, "C": 4.5, "E": 2.5, "A": 2.5, "ES": 4.0},
            difficulty_level="mid"
        ),
        
        Job(
            id="job_003",
            title="DevOps Engineer",
            industry="Technology",
            description="Build and maintain reliable infrastructure",
            ideal_work_type="UMSETZER",
            ideal_social_type="BEOBACHTER",
            ideal_archetype="STITCHER",
            salary_range=(85000, 155000),
            growth_potential=0.8,
            work_life_balance=0.5,
            remote_friendly=True,
            team_size="small",
            required_skills=["systems", "automation", "reliability", "monitoring"],
            big_five_profile={"O": 3.0, "C": 4.5, "E": 2.0, "A": 3.0, "ES": 3.5},
            difficulty_level="mid"
        ),
        
        # Leadership & Management
        Job(
            id="job_004",
            title="Engineering Manager",
            industry="Technology",
            description="Lead and develop engineering teams",
            ideal_work_type="ORGANISATEUR",
            ideal_social_type="MODERATOR",
            ideal_archetype="HOT_PERSON",
            salary_range=(120000, 200000),
            growth_potential=0.9,
            work_life_balance=0.6,
            remote_friendly=True,
            team_size="medium",
            required_skills=["leadership", "people management", "strategy", "communication"],
            big_five_profile={"O": 3.5, "C": 4.0, "E": 4.5, "A": 4.0, "ES": 4.5},
            difficulty_level="senior"
        ),
        
        Job(
            id="job_005",
            title="HR Manager",
            industry="Human Resources",
            description="Manage people, culture, and development",
            ideal_work_type="ORGANISATEUR",
            ideal_social_type="MODERATOR",
            ideal_archetype="HOT_PERSON",
            salary_range=(70000, 120000),
            growth_potential=0.75,
            work_life_balance=0.8,
            remote_friendly=True,
            team_size="medium",
            required_skills=["people skills", "empathy", "communication", "strategy"],
            big_five_profile={"O": 3.5, "C": 3.5, "E": 4.5, "A": 4.5, "ES": 4.0},
            difficulty_level="mid"
        ),
        
        # Analysis & Strategy
        Job(
            id="job_006",
            title="Business Analyst",
            industry="Consulting",
            description="Analyze business processes and recommend improvements",
            ideal_work_type="ANALYTIKER",
            ideal_social_type="PARTNER",
            ideal_archetype="GROWN_UP",
            salary_range=(75000, 130000),
            growth_potential=0.85,
            work_life_balance=0.65,
            remote_friendly=True,
            team_size="medium",
            required_skills=["analysis", "communication", "business acumen", "detail"],
            big_five_profile={"O": 3.5, "C": 4.5, "E": 3.5, "A": 3.5, "ES": 4.0},
            difficulty_level="mid"
        ),
        
        Job(
            id="job_007",
            title="Strategy Consultant",
            industry="Consulting",
            description="Develop strategic recommendations for clients",
            ideal_work_type="DENKER",
            ideal_social_type="INDIVIDUALIST",
            ideal_archetype="SLOP_CANNON",
            salary_range=(100000, 200000),
            growth_potential=0.9,
            work_life_balance=0.5,
            remote_friendly=True,
            team_size="small",
            required_skills=["strategic thinking", "analysis", "communication", "creativity"],
            big_five_profile={"O": 4.5, "C": 3.5, "E": 4.0, "A": 3.0, "ES": 4.5},
            difficulty_level="senior"
        ),
        
        # Sales & Business Development
        Job(
            id="job_008",
            title="Sales Manager",
            industry="Sales",
            description="Build and lead sales teams to hit targets",
            ideal_work_type="VERKÄUFER",
            ideal_social_type="MODERATOR",
            ideal_archetype="HOT_PERSON",
            salary_range=(80000, 200000),
            growth_potential=0.85,
            work_life_balance=0.5,
            remote_friendly=False,
            team_size="medium",
            required_skills=["sales", "leadership", "communication", "persuasion"],
            big_five_profile={"O": 3.5, "C": 3.0, "E": 4.5, "A": 3.5, "ES": 4.0},
            difficulty_level="mid"
        ),
        
        # Finance & Operations
        Job(
            id="job_009",
            title="Financial Analyst",
            industry="Finance",
            description="Analyze financial data and create forecasts",
            ideal_work_type="ANALYTIKER",
            ideal_social_type="BEOBACHTER",
            ideal_archetype="STITCHER",
            salary_range=(70000, 120000),
            growth_potential=0.75,
            work_life_balance=0.75,
            remote_friendly=True,
            team_size="small",
            required_skills=["financial analysis", "excel", "attention to detail", "numbers"],
            big_five_profile={"O": 2.5, "C": 4.5, "E": 2.0, "A": 2.5, "ES": 3.5},
            difficulty_level="mid"
        ),
        
        # Creative
        Job(
            id="job_010",
            title="UX/UI Designer",
            industry="Technology",
            description="Design beautiful and usable interfaces",
            ideal_work_type="DENKER",
            ideal_social_type="INDIVIDUALIST",
            ideal_archetype="SLOP_CANNON",
            salary_range=(75000, 140000),
            growth_potential=0.8,
            work_life_balance=0.7,
            remote_friendly=True,
            team_size="small",
            required_skills=["design", "creativity", "empathy", "prototyping"],
            big_five_profile={"O": 4.5, "C": 3.5, "E": 3.0, "A": 3.5, "ES": 4.0},
            difficulty_level="mid"
        ),
    ]
    
    # ==================== MATCHING ALGORITHM ====================
    
    @classmethod
    def calculate_job_fit_score(
        cls,
        personality_profile: Dict[str, float],
        work_type: str,
        social_type: str,
        archetype: str,
        job: Job
    ) -> float:
        """
        Calculate how well personality matches a job
        Uses multiple scoring dimensions
        
        Args:
            personality_profile: Big Five scores
            work_type: Work type (e.g., "DENKER")
            social_type: Social type (e.g., "MODERATOR")
            archetype: Functional archetype
            job: Job to match against
        
        Returns:
            Fit score (0-1)
        """
        scores = []
        weights = []
        
        # 1. Work Type Match (40%)
        work_type_match = 1.0 if work_type == job.ideal_work_type else 0.5
        scores.append(work_type_match)
        weights.append(0.40)
        
        # 2. Social Type Match (20%)
        social_type_match = 1.0 if social_type == job.ideal_social_type else 0.6
        scores.append(social_type_match)
        weights.append(0.20)
        
        # 3. Archetype Match (20%)
        archetype_match = 1.0 if archetype == job.ideal_archetype else 0.5
        scores.append(archetype_match)
        weights.append(0.20)
        
        # 4. Big Five Profile Match (20%)
        if SKLEARN_AVAILABLE:
            # Use cosine similarity for Big Five
            user_profile = np.array([
                personality_profile.get("O", 3.0),
                personality_profile.get("C", 3.0),
                personality_profile.get("E", 3.0),
                personality_profile.get("A", 3.0),
                personality_profile.get("ES", 3.0)
            ]).reshape(1, -1)
            
            job_profile = np.array([
                job.big_five_profile.get("O", 3.0),
                job.big_five_profile.get("C", 3.0),
                job.big_five_profile.get("E", 3.0),
                job.big_five_profile.get("A", 3.0),
                job.big_five_profile.get("ES", 3.0)
            ]).reshape(1, -1)
            
            # Normalize
            scaler = StandardScaler()
            user_profile = scaler.fit_transform(user_profile)
            job_profile = scaler.transform(job_profile)
            
            similarity = cosine_similarity(user_profile, job_profile)[0][0]
            # Convert from [-1, 1] to [0, 1]
            big_five_match = (similarity + 1) / 2
        else:
            # Fallback: simple difference
            diff = sum(abs(personality_profile.get(k, 3.0) - job.big_five_profile.get(k, 3.0))
                      for k in ["O", "C", "E", "A", "ES"])
            big_five_match = max(0, 1 - (diff / 20))  # Normalize
        
        scores.append(big_five_match)
        weights.append(0.20)
        
        # Calculate weighted average
        total_score = sum(s * w for s, w in zip(scores, weights))
        return min(1.0, max(0.0, total_score))
    
    # ==================== RECOMMENDATION ====================
    
    @classmethod
    def get_top_jobs(
        cls,
        personality_profile: Dict[str, float],
        work_type: str,
        social_type: str,
        archetype: str,
        top_n: int = 5
    ) -> List[Dict[str, any]]:
        """
        Get top job recommendations for a personality profile
        
        Args:
            personality_profile: Big Five scores (O, C, E, A, ES)
            work_type: Work type
            social_type: Social type
            archetype: Functional archetype
            top_n: Number of recommendations to return
        
        Returns:
            List of top job matches with scores
        """
        job_scores = []
        
        for job in cls.JOB_DATABASE:
            fit_score = cls.calculate_job_fit_score(
                personality_profile,
                work_type,
                social_type,
                archetype,
                job
            )
            
            job_scores.append({
                "id": job.id,
                "title": job.title,
                "industry": job.industry,
                "fit_score": round(fit_score, 2),
                "salary_range": job.salary_range,
                "growth_potential": job.growth_potential,
                "work_life_balance": job.work_life_balance,
                "remote_friendly": job.remote_friendly,
                "ideal_archetype": job.ideal_archetype,
                "reasoning": cls._generate_reasoning(
                    fit_score, work_type, job.ideal_work_type, archetype, job.ideal_archetype
                )
            })
        
        # Sort by fit score descending
        job_scores.sort(key=lambda x: x["fit_score"], reverse=True)
        
        # Return top N
        return job_scores[:top_n]
    
    # ==================== REASONING ====================
    
    @staticmethod
    def _generate_reasoning(
        fit_score: float,
        work_type: str,
        ideal_work_type: str,
        archetype: str,
        ideal_archetype: str
    ) -> str:
        """Generate human-readable reasoning for job match"""
        reasons = []
        
        if fit_score > 0.85:
            reasons.append("Excellent match for your profile")
        elif fit_score > 0.75:
            reasons.append("Very good match for your profile")
        elif fit_score > 0.65:
            reasons.append("Good match for your profile")
        else:
            reasons.append("Moderate match for your profile")
        
        if work_type == ideal_work_type:
            reasons.append(f"Your {work_type} work style aligns perfectly")
        
        if archetype == ideal_archetype:
            reasons.append(f"Your {archetype} archetype is ideal for this role")
        
        return ". ".join(reasons) + "."
    
    # ==================== BATCH PROCESSING ====================
    
    @classmethod
    def get_industry_recommendations(cls, industry: str) -> List[Job]:
        """
        Get all jobs in a specific industry
        
        Args:
            industry: Industry name
        
        Returns:
            List of jobs in that industry
        """
        return [job for job in cls.JOB_DATABASE if job.industry.lower() == industry.lower()]
    
    @classmethod
    def search_jobs_by_archetype(cls, archetype: str) -> List[Job]:
        """
        Find all jobs ideal for a specific archetype
        
        Args:
            archetype: Archetype name
        
        Returns:
            List of matching jobs
        """
        return [job for job in cls.JOB_DATABASE if job.ideal_archetype == archetype]
    
    @classmethod
    def get_high_growth_jobs(cls, min_growth: float = 0.85) -> List[Job]:
        """
        Get high-growth potential jobs
        
        Args:
            min_growth: Minimum growth potential (0-1)
        
        Returns:
            List of high-growth jobs
        """
        return [job for job in cls.JOB_DATABASE if job.growth_potential >= min_growth]
    
    @classmethod
    def get_remote_friendly_jobs(cls) -> List[Job]:
        """Get all remote-friendly jobs"""
        return [job for job in cls.JOB_DATABASE if job.remote_friendly]
