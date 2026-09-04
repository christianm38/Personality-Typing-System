"""
Role Fit Prediction Engine
Machine Learning-based role prediction and success probability modeling
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np
import logging

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class Role:
    """Job role for prediction"""
    id: str
    title: str
    category: str
    level: str  # entry, mid, senior, lead
    required_dimensions: Dict[str, Tuple[float, float]]  # dimension: (min, max)
    success_factors: Dict[str, float]  # factor: weight


class RoleFitPredictionEngine:
    """
    ML-powered role fit prediction
    Predicts success probability in specific roles
    """
    
    # ==================== ROLE DATABASE ====================
    
    ROLE_DATABASE: Dict[str, Role] = {
        # Entry Level Roles
        "junior_engineer": Role(
            id="role_001",
            title="Junior Engineer",
            category="Technology",
            level="entry",
            required_dimensions={
                "O": (2.5, 5.0),  # Openness: moderate to high
                "C": (3.0, 5.0),  # Conscientiousness: moderate to high
                "E": (2.0, 5.0),  # Extraversion: flexible
                "A": (2.0, 5.0),  # Agreeableness: flexible
                "ES": (3.0, 5.0)  # Emotional Stability: moderate to high
            },
            success_factors={
                "technical_aptitude": 0.30,
                "learning_ability": 0.25,
                "attention_to_detail": 0.20,
                "collaboration": 0.15,
                "communication": 0.10
            }
        ),
        
        "analyst": Role(
            id="role_002",
            title="Analyst (Data/Business)",
            category="Analysis",
            level="entry",
            required_dimensions={
                "O": (2.5, 4.5),
                "C": (3.5, 5.0),
                "E": (1.5, 4.0),
                "A": (2.5, 4.5),
                "ES": (3.0, 5.0)
            },
            success_factors={
                "analytical_thinking": 0.35,
                "attention_to_detail": 0.25,
                "technical_skills": 0.20,
                "communication": 0.15,
                "patience": 0.05
            }
        ),
        
        # Mid Level Roles
        "senior_engineer": Role(
            id="role_003",
            title="Senior Engineer",
            category="Technology",
            level="mid",
            required_dimensions={
                "O": (3.0, 5.0),  # Innovation
                "C": (3.5, 5.0),  # Reliability
                "E": (2.5, 4.5),  # Some communication
                "A": (2.5, 4.5),  # Team work
                "ES": (3.5, 5.0)  # Stress handling
            },
            success_factors={
                "technical_depth": 0.35,
                "mentorship": 0.20,
                "problem_solving": 0.20,
                "leadership": 0.15,
                "communication": 0.10
            }
        ),
        
        "product_manager": Role(
            id="role_004",
            title="Product Manager",
            category="Product",
            level="mid",
            required_dimensions={
                "O": (3.5, 5.0),  # Creativity & innovation
                "C": (3.0, 4.5),  # Organization
                "E": (3.5, 5.0),  # Communication
                "A": (3.0, 4.5),  # Empathy
                "ES": (3.5, 5.0)  # Handling pressure
            },
            success_factors={
                "strategic_thinking": 0.25,
                "communication": 0.20,
                "technical_understanding": 0.20,
                "people_skills": 0.20,
                "decision_making": 0.15
            }
        ),
        
        "team_lead": Role(
            id="role_005",
            title="Team Lead",
            category="Leadership",
            level="mid",
            required_dimensions={
                "O": (2.5, 4.5),
                "C": (3.5, 5.0),  # Organization
                "E": (3.5, 5.0),  # Communication
                "A": (3.5, 5.0),  # Empathy
                "ES": (3.5, 5.0)  # Handling conflict
            },
            success_factors={
                "leadership": 0.30,
                "people_management": 0.25,
                "decision_making": 0.20,
                "communication": 0.15,
                "emotional_intelligence": 0.10
            }
        ),
        
        # Senior Roles
        "staff_engineer": Role(
            id="role_006",
            title="Staff/Principal Engineer",
            category="Technology",
            level="senior",
            required_dimensions={
                "O": (3.5, 5.0),  # Innovation & vision
                "C": (3.0, 4.5),  # Follow through
                "E": (2.5, 4.0),  # Some communication needed
                "A": (2.5, 4.0),  # Independent
                "ES": (3.5, 5.0)  # Handle high pressure
            },
            success_factors={
                "technical_expertise": 0.35,
                "strategic_vision": 0.25,
                "mentorship": 0.20,
                "communication": 0.15,
                "leadership": 0.05
            }
        ),
        
        "director": Role(
            id="role_007",
            title="Director / VP",
            category="Leadership",
            level="senior",
            required_dimensions={
                "O": (3.0, 4.5),  # Vision
                "C": (3.5, 5.0),  # Planning
                "E": (4.0, 5.0),  # Communication (high)
                "A": (3.0, 4.5),  # Empathy
                "ES": (4.0, 5.0)  # Pressure handling
            },
            success_factors={
                "strategic_leadership": 0.30,
                "people_management": 0.25,
                "business_acumen": 0.20,
                "communication": 0.15,
                "decision_making": 0.10
            }
        ),
        
        # Specialized Roles
        "sales_executive": Role(
            id="role_008",
            title="Sales Executive",
            category="Sales",
            level="mid",
            required_dimensions={
                "O": (2.5, 4.5),
                "C": (2.5, 4.0),
                "E": (4.5, 5.0),  # High extraversion
                "A": (2.5, 4.0),
                "ES": (3.5, 5.0)
            },
            success_factors={
                "persuasion": 0.25,
                "communication": 0.25,
                "resilience": 0.20,
                "relationship_building": 0.20,
                "negotiation": 0.10
            }
        ),
        
        "designer": Role(
            id="role_009",
            title="Designer (UX/Visual)",
            category="Design",
            level="mid",
            required_dimensions={
                "O": (4.0, 5.0),  # High creativity
                "C": (2.5, 4.0),
                "E": (2.5, 4.0),
                "A": (3.0, 4.5),  # Empathy
                "ES": (3.0, 4.5)
            },
            success_factors={
                "creativity": 0.30,
                "user_empathy": 0.25,
                "attention_to_detail": 0.20,
                "technical_skills": 0.15,
                "communication": 0.10
            }
        ),
    }
    
    # ==================== PREDICTION ALGORITHM ====================
    
    @classmethod
    def predict_role_fit(
        cls,
        big_five: Dict[str, float],
        work_type: str,
        archetype: str,
        target_role_id: str
    ) -> Dict[str, any]:
        """
        Predict fit for a specific role
        
        Args:
            big_five: Big Five personality scores
            work_type: Work type classification
            archetype: Functional archetype
            target_role_id: Role to evaluate
        
        Returns:
            Prediction with confidence and reasoning
        """
        if target_role_id not in cls.ROLE_DATABASE:
            return {"error": f"Role {target_role_id} not found"}
        
        role = cls.ROLE_DATABASE[target_role_id]
        
        # Score components
        dimension_fit = cls._score_dimension_fit(big_five, role)
        success_probability = cls._predict_success_probability(big_five, work_type, role)
        archetype_fit = cls._score_archetype_role_fit(archetype, role)
        
        # Calculate overall fit
        overall_fit = (
            dimension_fit * 0.40 +
            success_probability * 0.35 +
            archetype_fit * 0.25
        )
        
        return {
            "role_id": target_role_id,
            "role_title": role.title,
            "overall_fit_score": round(min(1.0, overall_fit), 2),
            "dimension_fit": round(dimension_fit, 2),
            "success_probability": round(success_probability, 2),
            "archetype_fit": round(archetype_fit, 2),
            "confidence_level": cls._get_confidence_level(overall_fit),
            "strengths_for_role": cls._identify_strengths_for_role(big_five, work_type, role),
            "development_areas": cls._identify_development_areas(big_five, work_type, role),
            "reasoning": cls._generate_fit_reasoning(overall_fit, role.title),
            "success_timeline": cls._estimate_success_timeline(overall_fit, role.level)
        }
    
    # ==================== SCORING FUNCTIONS ====================
    
    @staticmethod
    def _score_dimension_fit(big_five: Dict[str, float], role: Role) -> float:
        """
        Score how well Big Five dimensions match role requirements
        
        Args:
            big_five: Personality scores
            role: Target role
        
        Returns:
            Fit score (0-1)
        """
        scores = []
        
        for dimension, (min_val, max_val) in role.required_dimensions.items():
            actual = big_five.get(dimension, 3.0)
            
            # Score based on range fit
            if min_val <= actual <= max_val:
                # Within range - full points
                score = 1.0
            else:
                # Outside range - penalty based on distance
                if actual < min_val:
                    penalty = (min_val - actual) / 5  # Max penalty = 1
                else:
                    penalty = (actual - max_val) / 5
                score = max(0, 1 - penalty)
            
            scores.append(score)
        
        # Average across dimensions
        return sum(scores) / len(scores) if scores else 0.5
    
    @classmethod
    def _predict_success_probability(cls, big_five: Dict[str, float], work_type: str, role: Role) -> float:
        """
        Predict probability of success in role using ML
        
        Args:
            big_five: Personality scores
            work_type: Work type
            role: Target role
        
        Returns:
            Success probability (0-1)
        """
        if not SKLEARN_AVAILABLE:
            return cls._predict_success_probability_fallback(big_five, role)
        
        try:
            # Prepare features
            features = np.array([[
                big_five.get("O", 3.0),
                big_five.get("C", 3.0),
                big_five.get("E", 3.0),
                big_five.get("A", 3.0),
                big_five.get("ES", 3.0)
            ]])
            
            # Normalize
            scaler = StandardScaler()
            features_normalized = scaler.fit_transform(features)
            
            # Simple heuristic: distance from ideal profile
            # Build ideal profile from role requirements
            ideal_profile = np.array([[
                np.mean([min_v, max_v]) for min_v, max_v in role.required_dimensions.values()
            ]])
            
            ideal_normalized = scaler.transform(ideal_profile)
            
            # Calculate similarity
            distance = np.linalg.norm(features_normalized - ideal_normalized)
            similarity = 1 / (1 + distance)  # Sigmoid-like conversion
            
            return float(similarity)
        
        except Exception as e:
            logger.error(f"ML prediction error: {e}")
            return cls._predict_success_probability_fallback(big_five, role)
    
    @staticmethod
    def _predict_success_probability_fallback(big_five: Dict[str, float], role: Role) -> float:
        """Fallback success prediction without ML"""
        # Calculate mean error from ideal range
        errors = []
        
        for dimension, (min_val, max_val) in role.required_dimensions.items():
            actual = big_five.get(dimension, 3.0)
            ideal = (min_val + max_val) / 2
            error = abs(actual - ideal)
            errors.append(error)
        
        avg_error = sum(errors) / len(errors) if errors else 0
        # Convert error to probability
        probability = max(0, 1 - (avg_error / 5))
        return probability
    
    @classmethod
    def _score_archetype_role_fit(cls, archetype: str, role: Role) -> float:
        """Score how well archetype matches role"""
        archetype_role_fit = {
            # Slop Cannon fits innovation/speed roles
            "SLOP_CANNON": {
                "Product Manager": 0.9,
                "Director / VP": 0.7,
                "Senior Engineer": 0.85,
                "Designer (UX/Visual)": 0.8
            },
            # Stitcher fits ops/stability roles
            "STITCHER": {
                "Senior Engineer": 0.85,
                "Analyst (Data/Business)": 0.9,
                "Staff/Principal Engineer": 0.8
            },
            # Hot Person fits people roles
            "HOT_PERSON": {
                "Director / VP": 0.9,
                "Team Lead": 0.95,
                "Sales Executive": 0.85
            },
            # Grown-up fits advisory roles
            "GROWN_UP": {
                "Staff/Principal Engineer": 0.85,
                "Director / VP": 0.9,
                "Senior Engineer": 0.8
            }
        }
        
        fits = archetype_role_fit.get(archetype, {})
        fit_score = fits.get(role.title, 0.5)
        
        return fit_score
    
    # ==================== INSIGHTS ====================
    
    @staticmethod
    def _identify_strengths_for_role(big_five: Dict[str, float], work_type: str, role: Role) -> List[str]:
        """Identify what will make person successful in role"""
        strengths = []
        
        # Check Big Five
        if big_five.get("C", 0) >= 3.5 and "Conscientiousness" not in strengths:
            strengths.append("Strong organizational skills")
        
        if big_five.get("E", 0) >= 4.0:
            strengths.append("Strong communication ability")
        
        if big_five.get("O", 0) >= 4.0:
            strengths.append("Creative and innovative thinking")
        
        if big_five.get("A", 0) >= 3.5:
            strengths.append("Strong collaboration skills")
        
        if big_five.get("ES", 0) >= 4.0:
            strengths.append("Ability to handle pressure")
        
        # Work type specific
        if work_type == "DENKER":
            strengths.append("Strategic thinking and ideation")
        elif work_type == "ANALYTIKER":
            strengths.append("Deep analytical capabilities")
        elif work_type == "ORGANISATEUR":
            strengths.append("Leadership and coordination skills")
        
        return strengths[:3]  # Top 3
    
    @staticmethod
    def _identify_development_areas(big_five: Dict[str, float], work_type: str, role: Role) -> List[str]:
        """Identify areas to develop for role"""
        areas = []
        
        if big_five.get("C", 3) < 3.0:
            areas.append("Develop organizational and planning skills")
        
        if big_five.get("E", 3) < 3.5 and "extraversion" in role.title.lower():
            areas.append("Build communication and people skills")
        
        if big_five.get("ES", 3) < 3.5:
            areas.append("Develop resilience and stress management")
        
        if big_five.get("A", 3) < 3.0 and "Team" in role.title:
            areas.append("Improve collaboration and empathy")
        
        return areas[:3]  # Top 3
    
    @staticmethod
    def _generate_fit_reasoning(fit_score: float, role_title: str) -> str:
        """Generate human-readable reasoning"""
        if fit_score > 0.80:
            return f"Excellent fit for {role_title} - personality well-matched"
        elif fit_score > 0.70:
            return f"Good fit for {role_title} - should succeed with experience"
        elif fit_score > 0.60:
            return f"Moderate fit for {role_title} - will need development in areas"
        elif fit_score > 0.50:
            return f"Possible fit for {role_title} - but significant growth needed"
        else:
            return f"Poor fit for {role_title} - consider other roles"
    
    @staticmethod
    def _get_confidence_level(fit_score: float) -> str:
        """Get confidence level in prediction"""
        if fit_score > 0.80:
            return "Very High"
        elif fit_score > 0.65:
            return "High"
        elif fit_score > 0.55:
            return "Moderate"
        elif fit_score > 0.40:
            return "Low"
        else:
            return "Very Low"
    
    @staticmethod
    def _estimate_success_timeline(fit_score: float, role_level: str) -> str:
        """Estimate timeline to success in role"""
        level_months = {
            "entry": 3,
            "mid": 6,
            "senior": 9,
            "lead": 12
        }
        
        base_months = level_months.get(role_level, 6)
        
        if fit_score > 0.80:
            months = base_months // 2
        elif fit_score > 0.65:
            months = base_months
        elif fit_score > 0.50:
            months = int(base_months * 1.5)
        else:
            months = base_months * 2
        
        return f"{months} months to full productivity"
    
    # ==================== BATCH OPERATIONS ====================
    
    @classmethod
    def get_top_roles(cls, big_five: Dict[str, float], work_type: str, archetype: str, top_n: int = 5) -> List[Dict]:
        """Get top roles for a personality profile"""
        predictions = []
        
        for role_id in cls.ROLE_DATABASE.keys():
            prediction = cls.predict_role_fit(big_five, work_type, archetype, role_id)
            if "error" not in prediction:
                predictions.append(prediction)
        
        # Sort by overall fit
        predictions.sort(key=lambda x: x["overall_fit_score"], reverse=True)
        return predictions[:top_n]
    
    @classmethod
    def get_roles_by_level(cls, level: str) -> List[str]:
        """Get all roles at a specific level"""
        return [role_id for role_id, role in cls.ROLE_DATABASE.items() if role.level == level]
