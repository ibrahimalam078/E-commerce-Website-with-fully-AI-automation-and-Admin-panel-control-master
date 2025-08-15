"""
Configuration management for AI Automation System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Google Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDWCjgSYwWbsTEfg60uIWeg1f6YeSnr9tU')
    
    # Hugging Face
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ecommerce.db')
    
    # Cache
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'automation.log')
    
    # Model Configuration
    BLIP_MODEL_NAME = "Salesforce/blip-image-captioning-base"
    
    # AI Generation Settings
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Recommendation Settings
    MIN_RATINGS = 5
    N_RECOMMENDATIONS = 10
    
    # Price Prediction Settings
    PRICE_ADJUSTMENT_RANGE = 0.2  # 20% max adjustment
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        return True

# Validate configuration on import
Config.validate()
