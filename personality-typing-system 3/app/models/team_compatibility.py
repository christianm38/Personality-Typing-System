"""
Team Compatibility Engine
Machine Learning-based team analysis and compatibility scoring
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter
import numpy as np
import logging

try:
    from sklearn.metrics.pairwise import euclidean_distances
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class TeamMember:
    """Member of a team for analysis"""
    id: str
    name: str
    work_type: str
    social_type: str
    archetype: str
    big_five: Dict[str, float]
    role: str


class TeamCompatibilityEngine:
    """
    ML-powered team compatibility analysis
    Analyzes team composition and interpersonal dynamics
    """
    
    # ==================== TEAM SCORING ====================
    
    @classmethod
    def analyze_team_composition(cls, members: List[TeamMember]) -> Dict[str, any]:
        """
        Comprehensive analysis of team composition
        
        Args:
            members: List of team members
        
        Returns:
            Detailed team composition analysis
        """
        if not members:
            return {"error": "No team members provided"}
        
        analysis = {
            "team_size": len(members),
            "work_type_distribution": cls._analyze_work_types(members),
            "social_type_distribution": cls._analyze_social_types(members),
            "archetype_distribution": cls._analyze_archetypes(members),
            "big_five_team_profile": cls._calculate_team_big_five(members),
            "diversity_score": cls._calculate_diversity_score(members),
            "balance_score": cls._calculate_balance_score(members),
            "complementarity_score": cls._calculate_complementarity_score(members),
            "overall_health_score": 0.0,  # Calculated below
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Calculate overall health
        analysis["overall_health_score"] = (
            analysis["diversity_score"] * 0.3 +
            analysis["balance_score"] * 0.4 +
            analysis["complementarity_score"] * 0.3
        )
        
        # Generate insights
        analysis["strengths"] = cls._generate_team_strengths(analysis)
        analysis["weaknesses"] = cls._generate_team_weaknesses(analysis)
        analysis["recommendations"] = cls._generate_recommendations(analysis)
        
        return analysis
    
    # ==================== DISTRIBUTION ANALYSIS ====================
    
    @staticmethod
    def _analyze_work_types(members: List[TeamMember]) -> Dict[str, int]:
        """Analyze work type distribution"""
        work_types = [m.work_type for m in members]
        return dict(Counter(work_types))
    
    @staticmethod
    def _analyze_social_types(members: List[TeamMember]) -> Dict[str, int]:
        """Analyze social type distribution"""
        social_types = [m.social_type for m in members]
        return dict(Counter(social_types))
    
    @staticmethod
    def _analyze_archetypes(members: List[TeamMember]) -> Dict[str, int]:
        """Analyze archetype distribution"""
        archetypes = [m.archetype for m in members]
        return dict(Counter(archetypes))
    
    # ==================== BIG FIVE CALCULATION ====================
    
    @staticmethod
    def _calculate_team_big_five(members: List[TeamMember]) -> Dict[str, float]:
        """Calculate average Big Five for team"""
        dimensions = ["O", "C", "E", "A", "ES"]
        team_profile = {}
        
        for dim in dimensions:
            values = [m.big_five.get(dim, 3.0) for m in members]
            team_profile[dim] = round(sum(values) / len(values), 2)
        
        return team_profile
    
    # ==================== DIVERSITY SCORING ====================
    
    @classmethod
    def _calculate_diversity_score(cls, members: List[TeamMember]) -> float:
        """
        Calculate team diversity score (0-1)
        Higher = more diverse
        """
        if len(members) < 2:
            return 0.5
        
        # Count unique types
        work_types = set(m.work_type for m in members)
        social_types = set(m.social_type for m in members)
        archetypes = set(m.archetype for m in members)
        
        # Normalize by possible values
        work_diversity = len(work_types) / 5  # 5 work types
        social_diversity = len(social_types) / 4  # 4 social types
        archetype_diversity = len(archetypes) / 4  # 4 archetypes
        
        # Average diversity
        diversity = (work_diversity + social_diversity + archetype_diversity) / 3
        return round(min(1.0, diversity), 2)
    
    # ==================== BALANCE SCORING ====================
    
    @classmethod
    def _calculate_balance_score(cls, members: List[TeamMember]) -> float:
        """
        Calculate team balance score (0-1)
        Evaluates if types are evenly distributed
        """
        work_type_dist = cls._analyze_work_types(members)
        social_type_dist = cls._analyze_social_types(members)
        
        # Calculate standard deviation of distribution
        work_counts = list(work_type_dist.values())
        social_counts = list(social_type_dist.values())
        
        if not work_counts or not social_counts:
            return 0.5
        
        # Lower std dev = better balance
        work_std = np.std(work_counts)
        social_std = np.std(social_counts)
        
        # Normalize (lower values are better)
        # Max possible std for 5 types with n members ≈ n/2
        max_std = len(members) / 2
        
        work_balance = max(0, 1 - (work_std / max_std))
        social_balance = max(0, 1 - (social_std / max_std))
        
        balance = (work_balance + social_balance) / 2
        return round(min(1.0, balance), 2)
    
    # ==================== COMPLEMENTARITY SCORING ====================
    
    @classmethod
    def _calculate_complementarity_score(cls, members: List[TeamMember]) -> float:
        """
        Calculate how well members complement each other
        Uses Big Five profile compatibility
        """
        if len(members) < 2:
            return 0.5
        
        if not SKLEARN_AVAILABLE:
            return cls._calculate_complementarity_fallback(members)
        
        # Extract Big Five profiles
        profiles = []
        for member in members:
            profile = np.array([
                member.big_five.get("O", 3.0),
                member.big_five.get("C", 3.0),
                member.big_five.get("E", 3.0),
                member.big_five.get("A", 3.0),
                member.big_five.get("ES", 3.0)
            ])
            profiles.append(profile)
        
        profiles = np.array(profiles)
        
        # Normalize
        scaler = StandardScaler()
        profiles_normalized = scaler.fit_transform(profiles)
        
        # Calculate pairwise distances
        distances = euclidean_distances(profiles_normalized)
        
        # Average distance = complementarity
        # Higher distance = more different = more complementary
        avg_distance = np.mean(distances)
        
        # Normalize distance to 0-1
        # Max distance for 5-dim normalized = ~5
        complementarity = min(1.0, avg_distance / 3)
        
        return round(complementarity, 2)
    
    @staticmethod
    def _calculate_complementarity_fallback(members: List[TeamMember]) -> float:
        """Fallback calculation without scikit-learn"""
        total_diff = 0
        count = 0
        
        for i, m1 in enumerate(members):
            for m2 in members[i+1:]:
                diff = sum(abs(m1.big_five.get(k, 3.0) - m2.big_five.get(k, 3.0))
                          for k in ["O", "C", "E", "A", "ES"])
                total_diff += diff
                count += 1
        
        if count == 0:
            return 0.5
        
        avg_diff = total_diff / count
        # Normalize (max diff ≈ 10 per dimension)
        complementarity = min(1.0, avg_diff / 10)
        return round(complementarity, 2)
    
    # ==================== PAIRWISE COMPATIBILITY ====================
    
    @classmethod
    def calculate_pair_compatibility(cls, member1: TeamMember, member2: TeamMember) -> Dict[str, any]:
        """
        Calculate compatibility between two team members
        
        Args:
            member1: First team member
            member2: Second team member
        
        Returns:
            Compatibility analysis
        """
        # Same type compatibility
        same_work_type = member1.work_type == member2.work_type
        same_social_type = member1.social_type == member2.social_type
        same_archetype = member1.archetype == member2.archetype
        
        # Opposite type compatibility
        opposite_work = cls._are_work_types_complementary(member1.work_type, member2.work_type)
        opposite_social = cls._are_social_types_complementary(member1.social_type, member2.social_type)
        
        # Calculate score
        compatibility_score = 0.0
        
        if same_archetype:
            # Same archetype = strong synergy
            compatibility_score += 0.3
        elif opposite_work or opposite_social:
            # Complementary types
            compatibility_score += 0.25
        
        # Big Five distance
        big_five_diff = sum(abs(member1.big_five.get(k, 3.0) - member2.big_five.get(k, 3.0))
                           for k in ["O", "C", "E", "A", "ES"])
        
        # Moderate differences are good (not too similar, not too different)
        if 5 < big_five_diff < 12:
            compatibility_score += 0.4
        elif big_five_diff <= 5:
            compatibility_score += 0.25  # Too similar
        else:
            compatibility_score += 0.15  # Too different
        
        # Role diversity
        if member1.role != member2.role:
            compatibility_score += 0.3
        else:
            compatibility_score += 0.15
        
        return {
            "member1": member1.name,
            "member2": member2.name,
            "compatibility_score": round(min(1.0, compatibility_score), 2),
            "same_work_type": same_work_type,
            "same_social_type": same_social_type,
            "complementary": opposite_work or opposite_social,
            "reasoning": cls._generate_pair_reasoning(
                member1, member2, compatibility_score
            )
        }
    
    @staticmethod
    def _are_work_types_complementary(type1: str, type2: str) -> bool:
        """Check if two work types are complementary"""
        complementary_pairs = [
            ("DENKER", "UMSETZER"),
            ("ANALYTIKER", "ORGANISATEUR"),
            ("VERKÄUFER", "UMSETZER"),
        ]
        
        pair = tuple(sorted([type1, type2]))
        return any(tuple(sorted(cp)) == pair for cp in complementary_pairs)
    
    @staticmethod
    def _are_social_types_complementary(type1: str, type2: str) -> bool:
        """Check if two social types are complementary"""
        complementary_pairs = [
            ("MODERATOR", "BEOBACHTER"),
            ("INDIVIDUALIST", "PARTNER"),
        ]
        
        pair = tuple(sorted([type1, type2]))
        return any(tuple(sorted(cp)) == pair for cp in complementary_pairs)
    
    @staticmethod
    def _generate_pair_reasoning(member1: TeamMember, member2: TeamMember, score: float) -> str:
        """Generate reasoning for pair compatibility"""
        if score > 0.75:
            return f"{member1.name} and {member2.name} work very well together"
        elif score > 0.60:
            return f"{member1.name} and {member2.name} have good working compatibility"
        else:
            return f"{member1.name} and {member2.name} may need to adapt work styles"
    
    # ==================== INSIGHTS & RECOMMENDATIONS ====================
    
    @staticmethod
    def _generate_team_strengths(analysis: Dict) -> List[str]:
        """Generate list of team strengths"""
        strengths = []
        
        if analysis["diversity_score"] > 0.7:
            strengths.append("High team diversity brings multiple perspectives")
        
        if analysis["balance_score"] > 0.7:
            strengths.append("Well-balanced role distribution")
        
        if analysis["complementarity_score"] > 0.65:
            strengths.append("Members complement each other's strengths")
        
        # Check for representation of key archetypes
        archetypes = analysis["archetype_distribution"]
        if len(archetypes) == 4:
            strengths.append("All four archetypes represented on team")
        
        return strengths
    
    @staticmethod
    def _generate_team_weaknesses(analysis: Dict) -> List[str]:
        """Generate list of team weaknesses"""
        weaknesses = []
        
        if analysis["diversity_score"] < 0.5:
            weaknesses.append("Low team diversity - may lack different perspectives")
        
        if analysis["balance_score"] < 0.5:
            weaknesses.append("Imbalanced role distribution")
        
        if analysis["complementarity_score"] < 0.4:
            weaknesses.append("Team members may have conflicting work styles")
        
        # Check for missing archetypes
        if len(analysis["archetype_distribution"]) == 1:
            weaknesses.append("All members have similar archetype - adds risk")
        
        return weaknesses
    
    @staticmethod
    def _generate_recommendations(analysis: Dict) -> List[str]:
        """Generate recommendations for team improvement"""
        recommendations = []
        
        # Balance recommendations
        if analysis["balance_score"] < 0.6:
            recommendations.append("Consider adding members with underrepresented work types")
        
        # Diversity recommendations
        if analysis["diversity_score"] < 0.6:
            recommendations.append("Hire to increase team diversity and perspectives")
        
        # Complementarity
        if analysis["complementarity_score"] < 0.5:
            recommendations.append("Team members should work on bridging personality differences")
        
        # Structure
        if analysis["overall_health_score"] < 0.6:
            recommendations.append("Consider team restructuring or adding complementary members")
        else:
            recommendations.append("Team composition is healthy - focus on collaboration")
        
        return recommendations
    
    # ==================== TEAM ROLE ASSIGNMENT ====================
    
    @classmethod
    def suggest_role_assignments(cls, members: List[TeamMember]) -> Dict[str, str]:
        """
        Suggest optimal role assignments based on personality types
        
        Args:
            members: List of team members
        
        Returns:
            Dictionary of member -> suggested_role
        """
        role_suggestions = {}
        
        for member in members:
            if member.archetype == "SLOP_CANNON":
                suggested_role = "Product Lead / Innovator"
            elif member.archetype == "STITCHER":
                suggested_role = "Operations / Infrastructure Lead"
            elif member.archetype == "HOT_PERSON":
                suggested_role = "Team Lead / Manager"
            elif member.archetype == "GROWN_UP":
                suggested_role = "Senior Lead / Advisor"
            else:
                suggested_role = "Team Member"
            
            role_suggestions[member.name] = suggested_role
        
        return role_suggestions
