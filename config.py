import os
import json
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class Config:
    """Enhanced configuration management for the bot with persistence"""
    
    def __init__(self):
        self.config_file = "bot_config.json"
        self.config = {
            'bot_name': 'Kaala Billota',
            'version': '2.0.0',
            'default_prefix': '!',
            'embed_color': 0x5865F2,
            'max_message_length': 2000,
            'typing_timeout': 30,
            'rate_limit_window': 3600,
            'max_conversations_per_user': 100,
            'chat_frequency': 0.1,
            'personality_mode': 'friendly',
            'reactions_enabled': True,
            'random_chat_enabled': True,
            'mention_only': False,
            'custom_prompt_enabled': True,
            'anti_spam_enabled': True,
            'max_conversation_history': 10,
            'max_requests_per_minute': 30
        }
        self.load_config()
        self.load_from_env()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
                logger.info("Configuration loaded from file")
        except Exception as e:
            logger.error(f"Error loading configuration file: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved to file")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value and save to file"""
        self.config[key] = value
        self.save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self.config.copy()
    
    def update_settings(self, settings: Dict[str, Any]):
        """Update multiple settings at once"""
        self.config.update(settings)
        self.save_config()
        logger.info(f"Updated settings: {list(settings.keys())}")
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        default_config = {
            'bot_name': 'Kaala Billota',
            'version': '2.0.0',
            'default_prefix': '!',
            'embed_color': 0x5865F2,
            'max_message_length': 2000,
            'typing_timeout': 30,
            'rate_limit_window': 3600,
            'max_conversations_per_user': 100,
            'chat_frequency': 0.1,
            'personality_mode': 'friendly',
            'reactions_enabled': True,
            'random_chat_enabled': True,
            'mention_only': False,
            'custom_prompt_enabled': True,
            'anti_spam_enabled': True,
            'max_conversation_history': 10,
            'max_requests_per_minute': 30
        }
        self.config = default_config
        self.save_config()
        logger.info("Configuration reset to defaults")
    
    def get_bot_settings(self) -> Dict[str, Any]:
        """Get bot-specific settings"""
        return {
            'chat_frequency': self.config.get('chat_frequency', 0.1),
            'personality_mode': self.config.get('personality_mode', 'friendly'),
            'reactions_enabled': self.config.get('reactions_enabled', True),
            'random_chat_enabled': self.config.get('random_chat_enabled', True),
            'mention_only': self.config.get('mention_only', False),
            'custom_prompt_enabled': self.config.get('custom_prompt_enabled', True)
        }
    
    def update_bot_settings(self, settings: Dict[str, Any]):
        """Update bot-specific settings"""
        for key, value in settings.items():
            if key in ['chat_frequency', 'personality_mode', 'reactions_enabled', 
                      'random_chat_enabled', 'mention_only', 'custom_prompt_enabled']:
                self.config[key] = value
        
        self.save_config()
        logger.info(f"Updated bot settings: {list(settings.keys())}")
    
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security-specific settings"""
        return {
            'anti_spam_enabled': self.config.get('anti_spam_enabled', True),
            'max_message_length': self.config.get('max_message_length', 2000),
            'max_conversation_history': self.config.get('max_conversation_history', 10),
            'rate_limit_window': self.config.get('rate_limit_window', 60),
            'max_requests_per_minute': self.config.get('max_requests_per_minute', 30)
        }
    
    def update_security_settings(self, settings: Dict[str, Any]):
        """Update security-specific settings"""
        for key, value in settings.items():
            if key in ['anti_spam_enabled', 'max_message_length', 'max_conversation_history',
                      'rate_limit_window', 'max_requests_per_minute']:
                self.config[key] = value
        
        self.save_config()
        logger.info(f"Updated security settings: {list(settings.keys())}")
    
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
            
            # Chat settings
            if os.getenv('CHAT_FREQUENCY'):
                self.config['chat_frequency'] = float(os.getenv('CHAT_FREQUENCY'))
            
            if os.getenv('PERSONALITY_MODE'):
                self.config['personality_mode'] = os.getenv('PERSONALITY_MODE')
            
            logger.info("Configuration loaded from environment")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def export_config(self) -> str:
        """Export configuration as JSON string"""
        try:
            return json.dumps(self.config, indent=2)
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")
            return "{}"
    
    def import_config(self, config_json: str):
        """Import configuration from JSON string"""
        try:
            imported_config = json.loads(config_json)
            self.config.update(imported_config)
            self.save_config()
            logger.info("Configuration imported successfully")
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
