import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Config:
    """Persistent configuration management for the bot"""
    def __init__(self):
        self.config_file = "bot_config.json"
        self.config = {
            'chat_frequency': 0.1,
            'personality_mode': 'friendly',
            'reactions_enabled': True,
            'random_chat_enabled': True,
            'mention_only': False,
            'custom_prompt_enabled': True
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config.update(json.load(f))
                logger.info("Loaded config from file.")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")

    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("Saved config to file.")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()

    def get_all(self) -> Dict[str, Any]:
        return self.config.copy()

    def update(self, updates: Dict[str, Any]):
        self.config.update(updates)
        self.save_config()
