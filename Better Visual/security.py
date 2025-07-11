import hashlib
import time
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SecurityManager:
    """Security and anti-abuse system for the Discord bot"""
    
    def __init__(self):
        self.blocked_users = set()
        self.suspicious_activity = {}
        self.rate_limits = {}
        self.max_requests_per_minute = 30
        self.blocked_words = [
            'token', 'password', 'api_key', 'secret', 'private_key',
            'discord_token', 'bot_token', 'client_secret'
        ]
        
    def check_user_safety(self, user_id: str, message_content: str) -> tuple[bool, str]:
        """Check if user and message are safe"""
        # Check if user is blocked
        if user_id in self.blocked_users:
            return False, "User is blocked"
        
        # Check for suspicious content
        content_lower = message_content.lower()
        for word in self.blocked_words:
            if word in content_lower:
                logger.warning(f"Suspicious content from {user_id}: {word}")
                return False, f"Contains blocked word: {word}"
        
        # Check rate limiting
        if not self.check_rate_limit(user_id):
            return False, "Rate limit exceeded"
        
        return True, "OK"
    
    def check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limits"""
        current_time = time.time()
        
        if user_id not in self.rate_limits:
            self.rate_limits[user_id] = []
        
        # Remove old requests (older than 1 minute)
        self.rate_limits[user_id] = [
            req_time for req_time in self.rate_limits[user_id]
            if current_time - req_time < 60
        ]
        
        # Check if too many requests
        if len(self.rate_limits[user_id]) >= self.max_requests_per_minute:
            return False
        
        # Add current request
        self.rate_limits[user_id].append(current_time)
        return True
    
    def block_user(self, user_id: str, reason: str = "Manual block"):
        """Block a user"""
        self.blocked_users.add(user_id)
        logger.warning(f"User {user_id} blocked: {reason}")
    
    def unblock_user(self, user_id: str):
        """Unblock a user"""
        self.blocked_users.discard(user_id)
        logger.info(f"User {user_id} unblocked")
    
    def get_suspicious_activity(self, user_id: str) -> Dict:
        """Get suspicious activity for a user"""
        return self.suspicious_activity.get(user_id, {})
    
    def log_suspicious_activity(self, user_id: str, activity_type: str, details: str):
        """Log suspicious activity"""
        if user_id not in self.suspicious_activity:
            self.suspicious_activity[user_id] = {}
        
        if activity_type not in self.suspicious_activity[user_id]:
            self.suspicious_activity[user_id][activity_type] = []
        
        self.suspicious_activity[user_id][activity_type].append({
            'timestamp': time.time(),
            'details': details
        })
        
        logger.warning(f"Suspicious activity from {user_id}: {activity_type} - {details}")
    
    def sanitize_message(self, message: str) -> str:
        """Sanitize message content"""
        # Remove potential token-like strings
        import re
        # Remove strings that look like tokens (long alphanumeric strings)
        message = re.sub(r'\b[a-zA-Z0-9]{20,}\b', '[REDACTED]', message)
        return message
