import time
import logging
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

class RateLimiter:
    """Enhanced rate limiting for API calls and conversations with database integration"""
    
    def __init__(self, database=None):
        self.db = database
        self.limits = {
            'conversation': {'calls': 0, 'last_reset': time.time(), 'max': 50, 'window': 3600},  # 50 per hour
            'api_calls': {'calls': 0, 'last_reset': time.time(), 'max': 100, 'window': 3600},   # 100 per hour
            'daily': {'calls': 0, 'last_reset': time.time(), 'max': 1, 'window': 86400},        # 1 per day
            'images': {'calls': 0, 'last_reset': time.time(), 'max': 10, 'window': 86400}       # 10 per day
        }
        self.user_limits = {}
    
    def check_limit(self, user_id: str, limit_type: str) -> bool:
        """Check if user is within rate limits"""
        try:
            if limit_type not in self.limits:
                return True
            
            current_time = time.time()
            limit_config = self.limits[limit_type]
            
            # Reset counter if window has passed
            if current_time - limit_config['last_reset'] > limit_config['window']:
                limit_config['calls'] = 0
                limit_config['last_reset'] = current_time
            
            # Check if user has exceeded limit
            if limit_config['calls'] >= limit_config['max']:
                return False
            
            # Increment counter
            limit_config['calls'] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True
    
    def check_user_limit(self, user_id: str, limit_type: str, max_calls: int = 10, window: int = 3600) -> bool:
        """Check per-user rate limits with database integration"""
        try:
            current_time = time.time()
            
            # Use database if available for persistent tracking
            if self.db:
                usage_data = self.db.get_usage_data(user_id)
                
                if limit_type == 'api_calls':
                    # Check hourly API calls
                    if usage_data.get('hourly_calls', 0) >= 50:
                        return False
                    # Update usage in database
                    self.db.update_usage(user_id, 'api_call')
                    return True
                    
                elif limit_type == 'images':
                    # Check daily image generation
                    if usage_data.get('images_today', 0) >= 10:
                        return False
                    # Update usage in database
                    self.db.update_usage(user_id, 'image')
                    return True
                    
                elif limit_type == 'conversation':
                    # Check conversation limits (50 per hour)
                    if usage_data.get('hourly_calls', 0) >= 50:
                        return False
                    # Update usage in database
                    self.db.update_usage(user_id, 'api_call')
                    return True
            
            # Fallback to in-memory tracking
            if user_id not in self.user_limits:
                self.user_limits[user_id] = {}
            
            if limit_type not in self.user_limits[user_id]:
                self.user_limits[user_id][limit_type] = {
                    'calls': 0,
                    'last_reset': current_time
                }
            
            user_limit = self.user_limits[user_id][limit_type]
            
            # Reset counter if window has passed
            if current_time - user_limit['last_reset'] > window:
                user_limit['calls'] = 0
                user_limit['last_reset'] = current_time
            
            # Check if user has exceeded limit
            if user_limit['calls'] >= max_calls:
                return False
            
            # Increment counter
            user_limit['calls'] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error checking user rate limit: {e}")
            return True
    
    def get_usage_info(self, user_id: str) -> Dict:
        """Get detailed usage information for a user"""
        try:
            if self.db:
                usage_data = self.db.get_usage_data(user_id)
                
                # Calculate remaining limits
                api_calls_remaining = max(0, 50 - usage_data.get('hourly_calls', 0))
                images_remaining = max(0, 10 - usage_data.get('images_today', 0))
                
                return {
                    'api_calls': {
                        'used': usage_data.get('hourly_calls', 0),
                        'remaining': api_calls_remaining,
                        'limit': 50,
                        'reset_time': 'Every hour'
                    },
                    'images': {
                        'used': usage_data.get('images_today', 0),
                        'remaining': images_remaining,
                        'limit': 10,
                        'reset_time': 'Daily at midnight'
                    }
                }
            else:
                # Fallback to in-memory data
                return {
                    'api_calls': {
                        'used': 0,
                        'remaining': 50,
                        'limit': 50,
                        'reset_time': 'Every hour'
                    },
                    'images': {
                        'used': 0,
                        'remaining': 10,
                        'limit': 10,
                        'reset_time': 'Daily at midnight'
                    }
                }
                
        except Exception as e:
            logger.error(f"Error getting usage info: {e}")
            return {}
    
    def get_time_until_reset(self, limit_type: str) -> Optional[str]:
        """Get time until next reset for a limit type"""
        try:
            if limit_type not in self.limits:
                return None
            
            limit_config = self.limits[limit_type]
            current_time = time.time()
            time_since_reset = current_time - limit_config['last_reset']
            time_until_reset = limit_config['window'] - time_since_reset
            
            if time_until_reset <= 0:
                return "Now"
            
            hours = int(time_until_reset // 3600)
            minutes = int((time_until_reset % 3600) // 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
                
        except Exception as e:
            logger.error(f"Error getting reset time: {e}")
            return None
    
    def reset_limits(self):
        """Reset all rate limits (useful for testing)"""
        current_time = time.time()
        for limit_type in self.limits:
            self.limits[limit_type]['calls'] = 0
            self.limits[limit_type]['last_reset'] = current_time
        
        self.user_limits = {}
        logger.info("Rate limits reset")
    
    def reset_user_limits(self, user_id: str):
        """Reset limits for a specific user"""
        if user_id in self.user_limits:
            del self.user_limits[user_id]
            logger.info(f"Rate limits reset for user {user_id}")
