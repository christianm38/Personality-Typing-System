"""
NLP Processing Module
Analyzes open-ended survey responses using NLP
"""

import re
from typing import List, Dict, Tuple
import logging

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.sentiment import SentimentIntensityAnalyzer
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
    
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

logger = logging.getLogger(__name__)


class NLPProcessor:
    """
    Natural Language Processing for survey responses
    Extracts insights from open-ended questions
    """
    
    # ==================== KEYWORD DEFINITIONS ====================
    
    CAREER_KEYWORDS = {
        "innovation": ["innovate", "new", "creative", "invent", "design", "develop"],
        "analysis": ["analyze", "research", "data", "study", "investigate", "understand"],
        "management": ["manage", "lead", "organize", "coordinate", "direct", "oversee"],
        "people": ["team", "people", "collaborate", "communicate", "help", "support"],
        "execution": ["build", "implement", "execute", "deliver", "complete", "make"],
        "strategy": ["strategy", "plan", "vision", "goal", "objective", "direction"],
        "technical": ["code", "technical", "engineering", "system", "software", "technology"],
        "business": ["business", "market", "sales", "revenue", "profit", "customer"]
    }
    
    ENVIRONMENT_KEYWORDS = {
        "structured": ["structure", "rules", "process", "clear", "organized", "defined"],
        "flexible": ["flexible", "autonomy", "freedom", "independent", "creative", "dynamic"],
        "collaborative": ["team", "collaborate", "together", "group", "people", "social"],
        "autonomous": ["alone", "independent", "solo", "self-directed", "autonomous", "individual"],
        "fast": ["fast", "quick", "speed", "rapid", "urgent", "deadline"],
        "deep": ["deep", "detail", "thorough", "perfection", "quality", "meticulous"]
    }
    
    PERSONALITY_INDICATORS = {
        "extroverted": ["energy", "excited", "social", "people", "team", "group", "meeting"],
        "introverted": ["focus", "alone", "quiet", "independent", "solitude", "concentration"],
        "analytical": ["analyze", "data", "logic", "understand", "research", "investigate"],
        "creative": ["creative", "idea", "new", "innovate", "imagine", "design"],
        "organized": ["organized", "plan", "structure", "detail", "meticulous", "order"],
        "spontaneous": ["spontaneous", "flexible", "improvise", "adapt", "change", "quick"]
    }
    
    # ==================== SENTIMENT ANALYSIS ====================
    
    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment scores
        """
        if not NLTK_AVAILABLE:
            return {
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 0.5,
                "compound": 0.0
            }
        
        try:
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(text)
            
            return {
                "positive": scores["pos"],
                "negative": scores["neg"],
                "neutral": scores["neu"],
                "compound": scores["compound"]  # -1 to +1
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 0.5,
                "compound": 0.0
            }
    
    # ==================== KEYWORD EXTRACTION ====================
    
    @staticmethod
    def extract_keywords(text: str, keywords_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            keywords_dict: Dictionary of keyword categories
        
        Returns:
            Dictionary with found keywords per category
        """
        text_lower = text.lower()
        found_keywords = {}
        
        for category, keywords in keywords_dict.items():
            found = []
            for keyword in keywords:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(keyword)
            
            if found:
                found_keywords[category] = found
        
        return found_keywords
    
    # ==================== TEXT ANALYSIS ====================
    
    @classmethod
    def analyze_response(cls, text: str) -> Dict[str, any]:
        """
        Comprehensive analysis of an open-ended response
        
        Args:
            text: Survey response text
        
        Returns:
            Dictionary with analysis results
        """
        if not text or len(text.strip()) == 0:
            return {
                "text_length": 0,
                "word_count": 0,
                "sentiment": {"compound": 0},
                "career_interests": {},
                "environment_preferences": {},
                "personality_indicators": {},
                "energy_level": "neutral"
            }
        
        # Basic text metrics
        text_length = len(text)
        word_count = len(text.split())
        
        # Sentiment analysis
        sentiment = cls.analyze_sentiment(text)
        
        # Keyword extraction
        career_interests = cls.extract_keywords(text, cls.CAREER_KEYWORDS)
        environment = cls.extract_keywords(text, cls.ENVIRONMENT_KEYWORDS)
        personality = cls.extract_keywords(text, cls.PERSONALITY_INDICATORS)
        
        # Energy level from sentiment
        if sentiment["compound"] > 0.5:
            energy_level = "high"
        elif sentiment["compound"] < -0.2:
            energy_level = "low"
        else:
            energy_level = "neutral"
        
        return {
            "text_length": text_length,
            "word_count": word_count,
            "sentiment": sentiment,
            "career_interests": career_interests,
            "environment_preferences": environment,
            "personality_indicators": personality,
            "energy_level": energy_level,
            "keywords_found": sum(
                len(v) for v in career_interests.values()
            ) + sum(
                len(v) for v in environment.values()
            ) + sum(
                len(v) for v in personality.values()
            )
        }
    
    # ==================== DERIVED INSIGHTS ====================
    
    @classmethod
    def extract_career_interests(cls, text: str) -> List[str]:
        """
        Extract primary career interests from text
        
        Args:
            text: Response text
        
        Returns:
            List of career interests
        """
        analysis = cls.analyze_response(text)
        interests = []
        
        # Get primary interests
        career_dict = analysis["career_interests"]
        if "innovation" in career_dict:
            interests.append("innovation")
        if "people" in career_dict:
            interests.append("people_management")
        if "technical" in career_dict:
            interests.append("technical")
        if "strategy" in career_dict:
            interests.append("strategy")
        if "analysis" in career_dict:
            interests.append("analysis")
        
        return interests if interests else []
    
    @classmethod
    def extract_work_environment_preference(cls, text: str) -> str:
        """
        Determine preferred work environment
        
        Args:
            text: Response text
        
        Returns:
            Environment type (structured, flexible, collaborative, autonomous, mixed)
        """
        analysis = cls.analyze_response(text)
        env_dict = analysis["environment_preferences"]
        
        scores = {
            "structured": len(env_dict.get("structured", [])),
            "flexible": len(env_dict.get("flexible", [])),
            "collaborative": len(env_dict.get("collaborative", [])),
            "autonomous": len(env_dict.get("autonomous", [])),
            "fast": len(env_dict.get("fast", [])),
            "deep": len(env_dict.get("deep", []))
        }
        
        if max(scores.values()) == 0:
            return "mixed"
        
        # Combine scores
        structure_score = scores["structured"] + scores["deep"]
        flex_score = scores["flexible"] + scores["fast"]
        collab_score = scores["collaborative"]
        autono_score = scores["autonomous"]
        
        if structure_score > flex_score and structure_score > collab_score:
            return "structured"
        elif flex_score > structure_score and flex_score > collab_score:
            return "flexible"
        elif collab_score > autono_score:
            return "collaborative"
        elif autono_score > 0:
            return "autonomous"
        else:
            return "mixed"
    
    @classmethod
    def extract_communication_style(cls, text: str) -> str:
        """
        Infer communication style from response
        
        Args:
            text: Response text
        
        Returns:
            Communication style (verbose, concise, analytical, storytelling)
        """
        word_count = len(text.split())
        
        # Analyze structure
        sentences = text.split(".")
        avg_sentence_length = word_count / len(sentences) if sentences else 0
        
        # Check for keywords
        analytical_words = ["therefore", "because", "analyze", "data", "research"]
        story_words = ["realized", "learned", "discovered", "felt", "experience"]
        
        text_lower = text.lower()
        analytical_count = sum(1 for w in analytical_words if w in text_lower)
        story_count = sum(1 for w in story_words if w in text_lower)
        
        if analytical_count > story_count and word_count > 100:
            return "analytical"
        elif story_count > analytical_count:
            return "storytelling"
        elif avg_sentence_length > 20 and word_count > 150:
            return "verbose"
        elif word_count < 50:
            return "concise"
        else:
            return "balanced"


class ResponseInterpretation:
    """
    Interpret NLP analysis results in context of personality
    """
    
    @staticmethod
    def interpret_fulfillment_answer(analysis: Dict) -> Dict[str, any]:
        """
        Interpret what fulfills the person
        
        Args:
            analysis: NLP analysis from analyze_response
        
        Returns:
            Interpretation dictionary
        """
        return {
            "energy_level": analysis["energy_level"],
            "career_interests": analysis["career_interests"],
            "primary_motivation": NLPProcessor.extract_career_interests(
                analysis.get("text", "")
            ),
            "sentiment_score": analysis["sentiment"]["compound"]
        }
    
    @staticmethod
    def interpret_environment_answer(analysis: Dict) -> Dict[str, str]:
        """
        Interpret work environment preference
        
        Args:
            analysis: NLP analysis
        
        Returns:
            Environment preference summary
        """
        return {
            "primary_preference": analysis.get("environment_preferences", {}),
            "structure_need": "high" if "structured" in analysis.get("environment_preferences", {}) else "low"
        }
    
    @staticmethod
    def interpret_goals_answer(analysis: Dict) -> Dict[str, any]:
        """
        Interpret career goals from response
        
        Args:
            analysis: NLP analysis
        
        Returns:
            Goals interpretation
        """
        return {
            "clarity_level": "clear" if analysis["word_count"] > 30 else "vague",
            "sentiment": "positive" if analysis["sentiment"]["compound"] > 0 else "uncertain",
            "focus_areas": analysis["career_interests"]
        }
