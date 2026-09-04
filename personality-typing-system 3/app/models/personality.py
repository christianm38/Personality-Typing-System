"""
Personality Scoring Model
Implements Big Five assessment and Work/Social Type calculations
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import numpy as np
from app.config import settings


@dataclass
class BigFiveScores:
    """Big Five Personality Scores"""
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    emotional_stability: float
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "O": round(self.openness, 2),
            "C": round(self.conscientiousness, 2),
            "E": round(self.extraversion, 2),
            "A": round(self.agreeableness, 2),
            "ES": round(self.emotional_stability, 2)
        }
    
    def to_normalized(self) -> Dict[str, float]:
        """Get normalized scores (-1 to +1)"""
        return {
            "O": PersonalityTyping.normalize_score(self.openness),
            "C": PersonalityTyping.normalize_score(self.conscientiousness),
            "E": PersonalityTyping.normalize_score(self.extraversion),
            "A": PersonalityTyping.normalize_score(self.agreeableness),
            "ES": PersonalityTyping.normalize_score(self.emotional_stability)
        }


@dataclass
class PersonalityProfile:
    """Complete Personality Profile (all 3 layers)"""
    big_five: BigFiveScores
    work_type: str
    work_type_confidence: float
    social_type: str
    social_type_confidence: float
    work_social_combination: str
    primary_archetype: str
    all_archetypes: List[Tuple[str, float]]  # [(archetype, score), ...]


class PersonalityTyping:
    """
    Big Five → Work Types → Social Types Mapping
    Implements the 3-layer personality model
    """
    
    # ==================== WORK TYPE PROFILES ====================
    
    WORK_TYPE_PROFILES = {
        "DENKER": {
            "O": (0.70, 1.0),      # Offenheit: HIGH
            "C": (-1.0, -0.30),    # Gewissenhaftigkeit: LOW
            "E": (0.30, 1.0),      # Extraversion: HIGH
            "description": "Du bist innovativ und ideenreich",
            "color": "🔵",
            "characteristics": [
                "Generierst schnell neue Ideen",
                "Experimentierfreudig und flexibel",
                "Inspirierst andere mit Visionen",
                "Magst Vielfalt und Abwechslung",
                "Spontan und adaptiv"
            ],
            "in_teams": "Du bringst frische Perspektiven ein, magst aber klare Struktur von anderen",
            "to_improve": "Versuche, deine Ideen auch umzusetzen und nicht nur zu träumen"
        },
        
        "ANALYTIKER": {
            "O": (0.30, 1.0),      # Offenheit: HOCH-MITTEL
            "C": (0.30, 1.0),      # Gewissenhaftigkeit: HIGH
            "E": (-1.0, 0.30),     # Extraversion: LOW
            "description": "Du bist tiefgründig und qualitätsorientiert",
            "color": "🟣",
            "characteristics": [
                "Verstehst komplexe Systeme",
                "Recherchierst gründlich",
                "Höchste Qualitätsstandards",
                "Strukturiert und methodisch",
                "Verlässliche Arbeit"
            ],
            "in_teams": "Du bist der Garant für hohe Qualität, magst aber Zeit und Raum zum Denken",
            "to_improve": "Teile dein Wissen früher mit anderen, nicht erst nach Vollkommenheit"
        },
        
        "UMSETZER": {
            "O": (-1.0, 0.30),     # Offenheit: LOW
            "C": (0.30, 1.0),      # Gewissenhaftigkeit: HIGH
            "E": (-1.0, 0.30),     # Extraversion: LOW
            "description": "Du bist praktisch und effizient",
            "color": "🟠",
            "characteristics": [
                "Fokussiert auf konkrete Ergebnisse",
                "Zuverlässig und pünktlich",
                "Detailorientiert und präzise",
                "Machst gerne Pläne und hältst dich daran",
                "Deine Stärke: Durchführung"
            ],
            "in_teams": "Du sorgst für Struktur und Verlässlichkeit, brauchst aber klare Ziele",
            "to_improve": "Versuche, auch Raum für Experimente und Kreativität zu schaffen"
        },
        
        "ORGANISATEUR": {
            "O": (-1.0, 0.30),     # Offenheit: LOW
            "C": (0.30, 1.0),      # Gewissenhaftigkeit: HIGH
            "E": (0.30, 1.0),      # Extraversion: HIGH
            "description": "Du bist führungsstark und koordinativ",
            "color": "🟢",
            "characteristics": [
                "Strukturierst Teams und Prozesse",
                "Motivierst und inspirierst andere",
                "Kommunikativ und präsent",
                "Delegierst gerne und effektiv",
                "Verantwortungsvoll"
            ],
            "in_teams": "Du führst an, achte aber darauf, nicht zu kontrollierend zu wirken",
            "to_improve": "Lass anderen auch Raum zum Wachsen und zur Eigeninitiative"
        },
        
        "VERKÄUFER": {
            "O": (-1.0, 0.30),     # Offenheit: LOW
            "C": (-1.0, -0.30),    # Gewissenhaftigkeit: LOW
            "E": (0.30, 1.0),      # Extraversion: HIGH
            "description": "Du bist spontan und beziehungsorientiert",
            "color": "🔴",
            "characteristics": [
                "Charismatisch und kontaktfreudig",
                "Flexibel und pragmatisch",
                "Beziehungsorientiert",
                "Schnelle Improvisation",
                "Menschen-zentriert"
            ],
            "in_teams": "Du bringst Energie und Flexibilität, brauchst aber auch Struktur",
            "to_improve": "Versuche, dich mehr auf langfristige Planung zu konzentrieren"
        }
    }
    
    # ==================== SOCIAL TYPE PROFILES ====================
    
    SOCIAL_TYPE_PROFILES = {
        "MODERATOR": {
            "E": (0.20, 1.0),      # Extraversion: HIGH
            "A": (0.20, 1.0),      # Agreeableness: HIGH
            "description": "Du verbindest Menschen",
            "color": "💛",
            "characteristics": [
                "Diplomatisch und verständnisvoll",
                "Energiereich und sozial",
                "Moderierst Konflikte konstruktiv",
                "Konsens-orientiert",
                "Bringst beste aus anderen heraus"
            ],
            "collaboration": "Du brauchst ein warmes, unterstützendes Team um erfolgreich zu sein"
        },
        
        "INDIVIDUALIST": {
            "E": (0.20, 1.0),      # Extraversion: HIGH
            "A": (-1.0, -0.20),    # Agreeableness: LOW
            "description": "Du bist direkt und durchsetzungsstark",
            "color": "💪",
            "characteristics": [
                "Assertiv und energisch",
                "Treibst Veränderungen voran",
                "Klare, direkte Kommunikation",
                "Unabhängig und mutig",
                "Magst Kompetition"
            ],
            "collaboration": "Du brauchst starke Partner, die nicht einschüchtern lassen"
        },
        
        "PARTNER": {
            "E": (-1.0, -0.20),    # Extraversion: LOW
            "A": (0.20, 1.0),      # Agreeableness: HIGH
            "description": "Du bist loyal und unterstützend",
            "color": "💚",
            "characteristics": [
                "Zuverlässig und gewissenhaft",
                "Empathisch und einfühlsam",
                "Lange Beziehungen",
                "Höchste Loyalität",
                "Magst Harmonie"
            ],
            "collaboration": "Du brauchst Sicherheit und langfristige Bindung im Team"
        },
        
        "BEOBACHTER": {
            "E": (-1.0, -0.20),    # Extraversion: LOW
            "A": (-1.0, -0.20),    # Agreeableness: LOW
            "description": "Du bist kritisch und unabhängig",
            "color": "🔍",
            "characteristics": [
                "Hinterfragst und überprüfst",
                "Qualitätskontrolle",
                "Introspektiv und reflektiert",
                "Präzise und sachlich",
                "Magst Logik statt Emotion"
            ],
            "collaboration": "Du brauchst respekt-volle Distanz und Zeit für Analyse"
        }
    }
    
    # ==================== SCORING METHODS ====================
    
    @staticmethod
    def score_dimension(responses: List[int]) -> float:
        """
        Calculate average score for a Big Five dimension
        
        Args:
            responses: List of Likert responses (1-5)
        
        Returns:
            Average score (1-5)
        """
        if not responses:
            return 3.0  # Default neutral
        return np.mean(responses)
    
    @staticmethod
    def normalize_score(score: float, scale: float = 2.0) -> float:
        """
        Normalize score from 1-5 range to -1 to +1 range
        
        Args:
            score: Raw score (1-5)
            scale: Divisor (default 2.0)
        
        Returns:
            Normalized score (-1 to +1)
        """
        return (score - 3) / scale
    
    @classmethod
    def calculate_big_five(
        cls,
        O_responses: List[int],
        C_responses: List[int],
        E_responses: List[int],
        A_responses: List[int],
        ES_responses: List[int]
    ) -> BigFiveScores:
        """
        Calculate Big Five scores from responses
        
        Args:
            O_responses: Openness responses
            C_responses: Conscientiousness responses
            E_responses: Extraversion responses
            A_responses: Agreeableness responses
            ES_responses: Emotional Stability responses
        
        Returns:
            BigFiveScores object
        """
        return BigFiveScores(
            openness=cls.score_dimension(O_responses),
            conscientiousness=cls.score_dimension(C_responses),
            extraversion=cls.score_dimension(E_responses),
            agreeableness=cls.score_dimension(A_responses),
            emotional_stability=cls.score_dimension(ES_responses)
        )
    
    @classmethod
    def calculate_work_type(
        cls,
        O: float,
        C: float,
        E: float
    ) -> Tuple[str, float]:
        """
        Calculate Work Type from Big Five scores
        
        Args:
            O: Openness (1-5)
            C: Conscientiousness (1-5)
            E: Extraversion (1-5)
        
        Returns:
            Tuple of (work_type, confidence_score)
        """
        # Normalize
        O_norm = cls.normalize_score(O)
        C_norm = cls.normalize_score(C)
        E_norm = cls.normalize_score(E)
        
        # Calculate fit for each type
        best_fit = None
        best_score = -1
        
        for work_type, profile in cls.WORK_TYPE_PROFILES.items():
            score = cls._calculate_fit(
                {"O": O_norm, "C": C_norm, "E": E_norm},
                profile
            )
            if score > best_score:
                best_score = score
                best_fit = work_type
        
        # Confidence: wie gut passt dieser Typ?
        # Range: 0.65 - 0.95
        confidence = 0.65 + (best_score * 0.30)
        confidence = min(0.95, max(0.65, confidence))
        
        return best_fit, round(confidence, 2)
    
    @classmethod
    def calculate_social_type(
        cls,
        E: float,
        A: float
    ) -> Tuple[str, float]:
        """
        Calculate Social Type from Extraversion & Agreeableness
        
        Args:
            E: Extraversion (1-5)
            A: Agreeableness (1-5)
        
        Returns:
            Tuple of (social_type, confidence_score)
        """
        E_norm = cls.normalize_score(E)
        A_norm = cls.normalize_score(A)
        
        best_fit = None
        best_score = -1
        
        for social_type, profile in cls.SOCIAL_TYPE_PROFILES.items():
            score = cls._calculate_fit(
                {"E": E_norm, "A": A_norm},
                profile
            )
            if score > best_score:
                best_score = score
                best_fit = social_type
        
        confidence = 0.70 + (best_score * 0.25)
        confidence = min(0.95, max(0.70, confidence))
        
        return best_fit, round(confidence, 2)
    
    @staticmethod
    def _calculate_fit(scores: Dict[str, float], profile: Dict) -> float:
        """
        Calculate how well scores fit a profile
        
        Args:
            scores: Dictionary of normalized scores
            profile: Profile with dimension ranges
        
        Returns:
            Fit score (0-1)
        """
        fits = []
        for dim, (min_val, max_val) in profile.items():
            if dim not in scores:
                continue
            
            score = scores[dim]
            
            if min_val <= score <= max_val:
                # Perfect fit
                fits.append(1.0)
            else:
                # Distance from range
                if score < min_val:
                    distance = min_val - score
                else:
                    distance = score - max_val
                
                # Linear decay from distance
                fit_score = max(0, 1 - (distance * 0.3))
                fits.append(fit_score)
        
        return np.mean(fits) if fits else 0.5
    
    @classmethod
    def get_type_description(cls, type_name: str, type_category: str) -> Optional[Dict]:
        """
        Get description for a personality type
        
        Args:
            type_name: Name of the type (e.g., "DENKER")
            type_category: "work" or "social"
        
        Returns:
            Dictionary with type description or None
        """
        if type_category == "work":
            return cls.WORK_TYPE_PROFILES.get(type_name)
        elif type_category == "social":
            return cls.SOCIAL_TYPE_PROFILES.get(type_name)
        return None
    
    @classmethod
    def get_all_work_types(cls) -> List[str]:
        """Get all available work types"""
        return list(cls.WORK_TYPE_PROFILES.keys())
    
    @classmethod
    def get_all_social_types(cls) -> List[str]:
        """Get all available social types"""
        return list(cls.SOCIAL_TYPE_PROFILES.keys())
    
    @staticmethod
    def validate_responses(responses: List[int]) -> bool:
        """
        Validate survey responses
        
        Args:
            responses: List of Likert responses
        
        Returns:
            True if valid, False otherwise
        """
        if not responses:
            return False
        
        if len(responses) < settings.MIN_SURVEY_ANSWERS:
            return False
        
        # Check all values are 1-5
        for response in responses:
            if not isinstance(response, int) or response < 1 or response > 5:
                return False
        
        return True
