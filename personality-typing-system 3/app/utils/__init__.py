"""
Utils Package
Machine Learning utilities and helper functions
"""

try:
    from .nlp import NLPProcessor, ResponseInterpretation
except ImportError:
    NLPProcessor = None
    ResponseInterpretation = None

__all__ = [
    "NLPProcessor",
    "ResponseInterpretation",
]
