import time
from datetime import datetime, timedelta
from typing import Dict, DefaultDict
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Handle rate limiting for API calls and bot usage"""
    
    def __init__(self):
        # Store last request times for different limits
        self.api_call_times: DefaultDict[str, list] = defaultdict(list)
        self.conversation_times: DefaultDict[str, list] = defaultdict(list)
        
        # Rate limit configurations
        self.limits = {
            'api_calls': {
                'max_requests': 50,
                'time_window': 3600  # 1 hour in seconds
            },
            'conversation': {
                'max_requests': 5,
                'time_window': 60  # 1 minute in seconds
            }
        }
        
    def check_limit(self, user_id: str, limit_type: str) -> bool:
        """Check if user can make a request without hitting rate limits"""
        try:
            if limit_type not in self.limits:
                logger.warning(f"Unknown limit type: {limit_type}")
                return True
                
            limit_config = self.limits[limit_type]
            max_requests = limit_config['max_requests']
            time_window = limit_config['time_window']
            
            # Get the appropriate request times list
            if limit_type == 'api_calls':
                request_times = self.api_call_times[user_id]
            elif limit_type == 'conversation':
                request_times = self.conversation_times[user_id]
            else:
                return True
                
            current_time = time.time()
            
            # Remove old requests outside the time window
            cutoff_time = current_time - time_window
            request_times[:] = [t for t in request_times if t > cutoff_time]
            
            # Check if under the limit
            if len(request_times) < max_requests:
                # Add current request time
                request_times.append(current_time)
                return True
            else:
                logger.info(f"Rate limit hit for user {user_id}, type {limit_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Allow request on error
            
    def get_remaining_requests(self, user_id: str, limit_type: str) -> int:
        """Get remaining requests for a user and limit type"""
        try:
            if limit_type not in self.limits:
                return 0
                
            limit_config = self.limits[limit_type]
            max_requests = limit_config['max_requests']
            time_window = limit_config['time_window']
            
            # Get the appropriate request times list
            if limit_type == 'api_calls':
                request_times = self.api_call_times[user_id]
            elif limit_type == 'conversation':
                request_times = self.conversation_times[user_id]
            else:
                return max_requests
                
            current_time = time.time()
            cutoff_time = current_time - time_window
            
            # Count requests within time window
            recent_requests = [t for t in request_times if t > cutoff_time]
            
            return max(0, max_requests - len(recent_requests))
            
        except Exception as e:
            logger.error(f"Error getting remaining requests: {e}")
            return 0
            
    def get_reset_time(self, user_id: str, limit_type: str) -> datetime:
        """Get when the rate limit will reset for a user"""
        try:
            if limit_type not in self.limits:
                return datetime.now()
                
            limit_config = self.limits[limit_type]
            time_window = limit_config['time_window']
            
            # Get the appropriate request times list
            if limit_type == 'api_calls':
                request_times = self.api_call_times[user_id]
            elif limit_type == 'conversation':
                request_times = self.conversation_times[user_id]
            else:
                return datetime.now()
                
            if not request_times:
                return datetime.now()
                
            # Find the oldest request within the time window
            current_time = time.time()
            cutoff_time = current_time - time_window
            recent_requests = [t for t in request_times if t > cutoff_time]
            
            if recent_requests:
                oldest_request = min(recent_requests)
                reset_time = oldest_request + time_window
                return datetime.fromtimestamp(reset_time)
            else:
                return datetime.now()
                
        except Exception as e:
            logger.error(f"Error getting reset time: {e}")
            return datetime.now()
            
    def clear_user_limits(self, user_id: str):
        """Clear all rate limits for a user (admin function)"""
        try:
            if user_id in self.api_call_times:
                del self.api_call_times[user_id]
            if user_id in self.conversation_times:
                del self.conversation_times[user_id]
                
            logger.info(f"Cleared rate limits for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error clearing user limits: {e}")
            
    def get_user_stats(self, user_id: str) -> Dict:
        """Get rate limiting statistics for a user"""
        try:
            stats = {}
            
            for limit_type in self.limits:
                remaining = self.get_remaining_requests(user_id, limit_type)
                max_requests = self.limits[limit_type]['max_requests']
                reset_time = self.get_reset_time(user_id, limit_type)
                
                stats[limit_type] = {
                    'remaining': remaining,
                    'max': max_requests,
                    'used': max_requests - remaining,
                    'reset_time': reset_time.isoformat()
                }
                
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
