"""
Functional Archetypes Model
Implements Yoav Rechtman's AI-Era Archetypes Framework
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from app.config import settings


@dataclass
class ArchetypeScore:
    """Single Archetype Score"""
    archetype: str
    score: float  # 0-1
    reasoning: str
    alignment_type: str  # "natural_fit", "bonus", "calculated"


class ArchetypeCalculator:
    """
    Calculate functional archetypes based on personality profile
    """
    
    # ==================== ARCHETYPE DEFINITIONS ====================
    
    ARCHETYPE_CONFIGS = {
        "SLOP_CANNON": {
            "name": "🚀 Slop Cannon",
            "description": "Geschwindigkeit + AI + Umsetzung",
            "full_description": """
Du bist wertvoll wegen Geschwindigkeit, AI-Nutzung und schneller Umsetzung.
Du kannst KI-Tools nutzen, um in kurzer Zeit Produkte und Code zu bauen.
Deine Stärke: Iteration, Experimente, schnelle Prototypen.
            """,
            "natural_fits": [
                ("DENKER", "INDIVIDUALIST"),
                ("VERKÄUFER", "INDIVIDUALIST"),
                ("ORGANISATEUR", "INDIVIDUALIST"),
            ],
            "bonus_dimensions": settings.SLOP_CANNON_BONUS,
            "ideal_roles": [
                "Product Engineer",
                "Full-Stack Developer",
                "Technical PM",
                "Growth Hacker",
                "Startup Founder",
                "AI-Powered Builder"
            ],
            "skills_to_develop": [
                "AI Tool Proficiency (Claude, ChatGPT, etc.)",
                "Rapid Prototyping",
                "Systems Thinking",
                "Basic DevOps",
                "Product Thinking"
            ],
            "strengths": [
                "Schnelle Umsetzung",
                "Comfortable mit Unvollkommenheit",
                "Lernt schnell neue Tools",
                "Generalist Mindset",
                "Experimentierfreudig"
            ],
            "weaknesses": [
                "Kann zu chaotisch sein",
                "Qualität kann leiden",
                "Wenig langfristige Planung",
                "Technische Schulden"
            ],
            "ai_era_importance": "CRITICAL - Die Zukunft gehört denen, die AI am schnellsten nutzen"
        },
        
        "STITCHER": {
            "name": "🧵 Stitcher",
            "description": "Stabilität + Sicherheit + Technik",
            "full_description": """
Du bist wertvoll wegen Systemverständnis, Stabilität und Sicherheit.
Du machst all das von Slop Cannons produzierte Zeug stabil, sicher und zuverlässig.
Deine Stärke: Systemdesign, Infrastruktur, Qualitätskontrolle, Risikomanagement.
            """,
            "natural_fits": [
                ("ANALYTIKER", "BEOBACHTER"),
                ("UMSETZER", "PARTNER"),
                ("ANALYTIKER", "PARTNER"),
            ],
            "bonus_dimensions": settings.STITCHER_BONUS,
            "ideal_roles": [
                "Infrastructure Engineer",
                "SRE (Site Reliability Engineer)",
                "Security Specialist",
                "Quality Assurance Lead",
                "System Architect",
                "Database Administrator",
                "DevOps Engineer"
            ],
            "skills_to_develop": [
                "Cloud Architecture (AWS, GCP, Azure)",
                "Kubernetes & Containerization",
                "Security Frameworks (OAuth, encryption, etc.)",
                "System Design",
                "Monitoring & Observability"
            ],
            "strengths": [
                "Tiefes Systemverständnis",
                "Attention to Detail",
                "Risk Awareness",
                "Long-term Thinking",
                "Preventive Mindset"
            ],
            "weaknesses": [
                "Kann zu langsam sein",
                "Perfektionistisch",
                "Weniger innovativ",
                "Mag Risiken nicht"
            ],
            "ai_era_importance": "CRITICAL - AI macht schnell viel Müll, Stitcher halten es zusammen"
        },
        
        "HOT_PERSON": {
            "name": "🔥 Hot Person",
            "description": "Beziehungen + Charisma + Vertrauen",
            "full_description": """
Du bist wertvoll wegen Charisma, Beziehungen und Vertrauen.
Menschen wollen mit dir zusammenarbeiten. Du bist schwer zu automatisieren.
Deine Stärke: Sales, Customer Relations, Empathie, People Management.
            """,
            "natural_fits": [
                ("VERKÄUFER", "MODERATOR"),
                ("ORGANISATEUR", "MODERATOR"),
                ("DENKER", "MODERATOR"),
            ],
            "bonus_dimensions": settings.HOT_PERSON_BONUS,
            "ideal_roles": [
                "Sales Manager",
                "Customer Success Manager",
                "People/HR Manager",
                "Business Development",
                "Community Manager",
                "Product Manager (external focus)",
                "Founder/CEO"
            ],
            "skills_to_develop": [
                "Strategic Selling",
                "Emotional Intelligence",
                "Negotiation",
                "Public Speaking",
                "Active Listening"
            ],
            "strengths": [
                "Charisma & Presence",
                "Beziehungsaufbau",
                "Empathie",
                "Vertrauenswürdigkeit",
                "Motivationsfähigkeit"
            ],
            "weaknesses": [
                "Kann zu emotions-getrieben sein",
                "Wenig Detailausrichtung",
                "Weniger technisch",
                "Subjektive Entscheidungen"
            ],
            "ai_era_importance": "CRITICAL - Menschliche Beziehungen bleiben zentral, KI kann das nicht vollständig ersetzen"
        },
        
        "GROWN_UP": {
            "name": "🧑‍⚖️ Grown-Up",
            "description": "Erfahrung + Urteilskraft + Governance",
            "full_description": """
Du bist wertvoll wegen Erfahrung, Urteilskraft und Verantwortung.
Du sagst: "Moment – sollten wir das wirklich machen?"
Deine Stärke: Langfristige Perspektive, Risikobewusstsein, Governance, Urteil.
            """,
            "natural_fits": [
                ("ANALYTIKER", "PARTNER"),
                ("ORGANISATEUR", "PARTNER"),
                ("UMSETZER", "PARTNER"),
            ],
            "bonus_dimensions": settings.GROWN_UP_BONUS,
            "ideal_roles": [
                "Finance Manager",
                "Legal Counsel",
                "Compliance Officer",
                "Engineering Manager",
                "C-Level Executive",
                "Board Member",
                "Operations Director"
            ],
            "skills_to_develop": [
                "Strategic Thinking",
                "Financial Acumen",
                "Risk Management",
                "Legal/Compliance Knowledge",
                "Executive Leadership"
            ],
            "strengths": [
                "Strategisches Denken",
                "Urteilskraft",
                "Langfristperspektive",
                "Risikobewusstsein",
                "Verantwortung"
            ],
            "weaknesses": [
                "Kann bremsen",
                "Konservativ",
                "Weniger innovativ",
                "Slow Decision Making"
            ],
            "ai_era_importance": "CRITICAL - Jemand muss die Kontrolle haben, wenn KI extrem schnell wird"
        }
    }
    
    # ==================== CALCULATION METHODS ====================
    
    @classmethod
    def calculate_archetype_scores(
        cls,
        work_type: str,
        social_type: str,
        big_five: Dict[str, float]
    ) -> List[ArchetypeScore]:
        """
        Calculate archetype fit scores
        
        Args:
            work_type: Work type (e.g., "DENKER")
            social_type: Social type (e.g., "MODERATOR")
            big_five: Dictionary of Big Five scores
        
        Returns:
            List of ArchetypeScore objects, sorted by score descending
        """
        combination = (work_type, social_type)
        results = []
        
        for archetype_name, config in cls.ARCHETYPE_CONFIGS.items():
            # Base: Is this combination a natural fit?
            is_natural_fit = combination in config["natural_fits"]
            base_score = 0.85 if is_natural_fit else 0.50
            
            # Calculate bonus from Big Five
            bonus = cls._calculate_bonus(big_five, config["bonus_dimensions"])
            
            # Final score
            final_score = max(0.30, min(1.0, base_score + bonus))
            
            # Determine reasoning
            if is_natural_fit:
                reasoning = f"Natural fit for {archetype_name}: {work_type} + {social_type}"
                alignment_type = "natural_fit"
            else:
                reasoning = f"Calculated fit from Big Five dimensions"
                alignment_type = "calculated"
            
            score = ArchetypeScore(
                archetype=archetype_name,
                score=round(final_score, 2),
                reasoning=reasoning,
                alignment_type=alignment_type
            )
            results.append(score)
        
        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        return results
    
    @staticmethod
    def _calculate_bonus(
        big_five: Dict[str, float],
        bonus_weights: Dict[str, float]
    ) -> float:
        """
        Calculate bonus from Big Five scores
        
        Args:
            big_five: Dictionary of Big Five scores (1-5)
            bonus_weights: Weights for each dimension
        
        Returns:
            Bonus value (-0.5 to +0.5)
        """
        bonus = 0.0
        
        for dimension, weight in bonus_weights.items():
            score = big_five.get(dimension, 3.0)
            # Normalize to -1 to +1
            normalized = (score - 3) / 2
            bonus += normalized * weight
        
        # Clamp to reasonable range
        return max(-0.5, min(0.5, bonus))
    
    @classmethod
    def get_primary_archetype(
        cls,
        scores: List[ArchetypeScore]
    ) -> str:
        """
        Get primary archetype from scores
        
        Args:
            scores: List of ArchetypeScore objects
        
        Returns:
            Primary archetype name
        """
        if scores:
            return scores[0].archetype
        return "GROWN_UP"  # Default fallback
    
    @classmethod
    def get_archetype_config(cls, archetype: str) -> Optional[Dict]:
        """
        Get configuration for an archetype
        
        Args:
            archetype: Archetype name
        
        Returns:
            Configuration dictionary or None
        """
        return cls.ARCHETYPE_CONFIGS.get(archetype)
    
    @classmethod
    def get_archetype_description(cls, archetype: str) -> str:
        """
        Get description for an archetype
        
        Args:
            archetype: Archetype name
        
        Returns:
            Description string
        """
        config = cls.get_archetype_config(archetype)
        if config:
            return config["full_description"].strip()
        return f"Unknown archetype: {archetype}"
    
    @classmethod
    def get_all_archetypes(cls) -> List[str]:
        """Get all available archetypes"""
        return list(cls.ARCHETYPE_CONFIGS.keys())
    
    @classmethod
    def validate_archetype(cls, archetype: str) -> bool:
        """
        Validate if archetype exists
        
        Args:
            archetype: Archetype name
        
        Returns:
            True if valid, False otherwise
        """
        return archetype in cls.ARCHETYPE_CONFIGS


class ArchetypeAnalysis:
    """
    Advanced archetype analysis and recommendations
    """
    
    @staticmethod
    def get_team_archetype_distribution(
        team_members: List[Tuple[str, str, Dict]]  # [(work_type, social_type, big_five), ...]
    ) -> Dict[str, int]:
        """
        Analyze archetype distribution in a team
        
        Args:
            team_members: List of member profiles
        
        Returns:
            Count of each archetype in team
        """
        distribution = {arch: 0 for arch in ArchetypeCalculator.get_all_archetypes()}
        
        for work_type, social_type, big_five in team_members:
            scores = ArchetypeCalculator.calculate_archetype_scores(
                work_type, social_type, big_five
            )
            if scores:
                primary = scores[0].archetype
                distribution[primary] += 1
        
        return distribution
    
    @staticmethod
    def get_ideal_team_composition() -> Dict[str, float]:
        """
        Get ideal team composition percentages
        
        Returns:
            Dictionary of archetype: ideal_percentage
        """
        return {
            "SLOP_CANNON": 0.30,    # 30% Builders
            "STITCHER": 0.40,       # 40% Stability & Quality
            "HOT_PERSON": 0.10,     # 10% Relationships
            "GROWN_UP": 0.20        # 20% Governance
        }
    
    @staticmethod
    def analyze_team_balance(
        distribution: Dict[str, int],
        team_size: int
    ) -> Dict[str, any]:
        """
        Analyze how balanced a team is
        
        Args:
            distribution: Archetype counts
            team_size: Total team size
        
        Returns:
            Analysis dictionary
        """
        ideal = ArchetypeAnalysis.get_ideal_team_composition()
        imbalances = {}
        
        for archetype, ideal_pct in ideal.items():
            ideal_count = team_size * ideal_pct
            actual_count = distribution.get(archetype, 0)
            diff = actual_count - ideal_count
            imbalances[archetype] = {
                "ideal": ideal_count,
                "actual": actual_count,
                "difference": diff,
                "status": "balanced" if abs(diff) < 1 else ("excess" if diff > 0 else "deficit")
            }
        
        return imbalances
    
    @staticmethod
    def get_team_gaps(distribution: Dict[str, int]) -> List[str]:
        """
        Identify which archetypes are missing from team
        
        Args:
            distribution: Archetype counts
        
        Returns:
            List of missing archetype names
        """
        return [arch for arch, count in distribution.items() if count == 0]
