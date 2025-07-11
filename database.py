import json
import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    """Handle JSON file-based data storage"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.users_file = f'{self.data_dir}/users.json'
        self.usage_file = f'{self.data_dir}/usage.json'
        self.conversations_file = f'{self.data_dir}/conversations.json'
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize files
        self._init_files()
        
    def _init_files(self):
        """Initialize JSON files if they don't exist"""
        files = [
            (self.users_file, {}),
            (self.usage_file, {}),
            (self.conversations_file, {})
        ]
        
        for file_path, default_data in files:
            if not os.path.exists(file_path):
                self._write_json(file_path, default_data)
                
    def _read_json(self, file_path: str) -> Dict:
        """Safely read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error reading {file_path}: {e}")
            return {}
            
    def _write_json(self, file_path: str, data: Dict):
        """Safely write JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error writing {file_path}: {e}")
            
    def get_user(self, user_id: str) -> Dict:
        """Get user data, create if doesn't exist"""
        users = self._read_json(self.users_file)
        
        if user_id not in users:
            users[user_id] = {
                'coins': 1000,
                'last_daily': None,
                'personality_mode': 'default',
                'total_commands': 0,
                'created_at': datetime.now().isoformat()
            }
            self._write_json(self.users_file, users)
            
        return users[user_id]
        
    def update_user(self, user_id: str, data: Dict):
        """Update user data"""
        users = self._read_json(self.users_file)
        
        if user_id in users:
            users[user_id].update(data)
        else:
            users[user_id] = data
            
        self._write_json(self.users_file, users)
        
    def add_coins(self, user_id: str, amount: int) -> int:
        """Add coins to user, return new balance"""
        user_data = self.get_user(user_id)
        user_data['coins'] = user_data.get('coins', 0) + amount
        self.update_user(user_id, user_data)
        return user_data['coins']
        
    def spend_coins(self, user_id: str, amount: int) -> bool:
        """Spend coins if user has enough, return success"""
        user_data = self.get_user(user_id)
        current_coins = user_data.get('coins', 0)
        
        if current_coins >= amount:
            user_data['coins'] = current_coins - amount
            user_data['total_commands'] = user_data.get('total_commands', 0) + 1
            self.update_user(user_id, user_data)
            return True
        return False
        
    def can_claim_daily(self, user_id: str) -> bool:
        """Check if user can claim daily reward"""
        user_data = self.get_user(user_id)
        last_daily = user_data.get('last_daily')
        
        if not last_daily:
            return True
            
        last_daily_date = datetime.fromisoformat(last_daily).date()
        today = datetime.now().date()
        
        return today > last_daily_date
        
    def claim_daily(self, user_id: str) -> int:
        """Claim daily reward, return new balance"""
        if self.can_claim_daily(user_id):
            user_data = self.get_user(user_id)
            user_data['last_daily'] = datetime.now().isoformat()
            self.update_user(user_id, user_data)
            return self.add_coins(user_id, 100)
        return self.get_user(user_id).get('coins', 0)
        
    def transfer_coins(self, from_user: str, to_user: str, amount: int) -> bool:
        """Transfer coins between users"""
        if self.spend_coins(from_user, amount):
            self.add_coins(to_user, amount)
            return True
        return False
        
    def get_usage_data(self, user_id: str) -> Dict:
        """Get usage tracking data for user"""
        usage = self._read_json(self.usage_file)
        
        if user_id not in usage:
            usage[user_id] = {
                'api_calls_today': 0,
                'images_today': 0,
                'last_reset': datetime.now().date().isoformat(),
                'hourly_calls': 0,
                'hourly_reset': datetime.now().isoformat()
            }
            self._write_json(self.usage_file, usage)
            
        return usage[user_id]
        
    def update_usage(self, user_id: str, usage_type: str):
        """Update usage statistics"""
        usage = self._read_json(self.usage_file)
        user_usage = self.get_usage_data(user_id)
        
        now = datetime.now()
        today = now.date().isoformat()
        
        # Reset daily counters if new day
        if user_usage.get('last_reset') != today:
            user_usage['api_calls_today'] = 0
            user_usage['images_today'] = 0
            user_usage['last_reset'] = today
            
        # Reset hourly counter if new hour
        last_hourly = datetime.fromisoformat(user_usage.get('hourly_reset', now.isoformat()))
        if now - last_hourly >= timedelta(hours=1):
            user_usage['hourly_calls'] = 0
            user_usage['hourly_reset'] = now.isoformat()
            
        # Update counters
        if usage_type == 'api_call':
            user_usage['api_calls_today'] += 1
            user_usage['hourly_calls'] += 1
        elif usage_type == 'image':
            user_usage['images_today'] += 1
            
        usage[user_id] = user_usage
        self._write_json(self.usage_file, usage)
        
    def add_conversation(self, user_id: str, user_message: str, bot_response: str):
        """Add conversation to history (keep last 5)"""
        conversations = self._read_json(self.conversations_file)
        
        if user_id not in conversations:
            conversations[user_id] = []
            
        conversations[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response
        })
        
        # Keep only last 5 conversations
        conversations[user_id] = conversations[user_id][-5:]
        
        self._write_json(self.conversations_file, conversations)
        
    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history for user"""
        conversations = self._read_json(self.conversations_file)
        return conversations.get(user_id, [])
        
    def set_personality_mode(self, user_id: str, mode: str):
        """Set personality mode for user"""
        user_data = self.get_user(user_id)
        user_data['personality_mode'] = mode
        self.update_user(user_id, user_data)
