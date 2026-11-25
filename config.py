"""
Configuration module for the Telegram Voice-to-Text bot.
Loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration class."""
    
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Groq API Configuration (Whisper)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # Webhook Configuration
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'
    WEBHOOK_PORT = int(os.getenv('PORT', 8080))
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Temporary files directory
    TEMP_DIR = '/tmp' if ENVIRONMENT == 'production' else 'tmp'
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required in environment variables")
        
        return True
    
    @classmethod
    def validate_groq_config(cls):
        """Validate Groq API configuration."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required in environment variables")
        return True


# Validate configuration on import
Config.validate()
