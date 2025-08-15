"""
AI Automation Services Package
Provides easy access to all AI automation services
"""

from .gemini_service import GeminiService
from .blip_service import BLIPService
from .recommendation_service import RecommendationService

__all__ = ['GeminiService', 'BLIPService', 'RecommendationService']

# Version information
__version__ = '1.0.0'
__author__ = 'AI Assistant'
__description__ = 'AI-powered e-commerce automation system'
