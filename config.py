import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'
    WEBHOOK_PORT = int(os.getenv('PORT', 8080))
    
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    TEMP_DIR = '/tmp' if ENVIRONMENT == 'production' else 'tmp'
    
    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required in environment variables")
        
        return True
    
    @classmethod
    def validate_groq_config(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required in environment variables")
        return True


Config.validate()
