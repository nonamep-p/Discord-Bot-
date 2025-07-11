import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Config:
    """Configuration management for the bot"""
    
    def __init__(self):
        self.config = {
            'bot_name': 'Kaala Billota',
            'version': '2.0.0',
            'default_prefix': '!',
            'embed_color': 0x5865F2,
            'max_message_length': 2000,
            'typing_timeout': 30,
            'rate_limit_window': 3600,
            'max_conversations_per_user': 100
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self.config.copy()
    
    def load_from_env(self):
        """Load configuration from environment variables"""
        try:
            # Bot settings
            if os.getenv('BOT_NAME'):
                self.config['bot_name'] = os.getenv('BOT_NAME')
            
            if os.getenv('BOT_PREFIX'):
                self.config['default_prefix'] = os.getenv('BOT_PREFIX')
            
            # API settings
            if os.getenv('GROQ_API_KEY'):
                self.config['groq_api_key'] = os.getenv('GROQ_API_KEY')
            
            # Rate limiting
            if os.getenv('RATE_LIMIT_WINDOW'):
                self.config['rate_limit_window'] = int(os.getenv('RATE_LIMIT_WINDOW'))
            
            logger.info("Configuration loaded from environment")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
