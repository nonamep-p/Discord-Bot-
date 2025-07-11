import time
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiting for API calls and conversations"""

    def __init__(self):
        self.limits = {
            'conversation': {'calls': 0, 'last_reset': time.time(), 'max': 50, 'window': 3600},  # 50 per hour
            'api_calls': {'calls': 0, 'last_reset': time.time(), 'max': 100, 'window': 3600},   # 100 per hour
            'daily': {'calls': 0, 'last_reset': time.time(), 'max': 1, 'window': 86400}         # 1 per day
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
        """Check per-user rate limits"""
        try:
            current_time = time.time()

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

    def reset_limits(self):
        """Reset all rate limits (useful for testing)"""
        current_time = time.time()
        for limit_type in self.limits:
            self.limits[limit_type]['calls'] = 0
            self.limits[limit_type]['last_reset'] = current_time

        self.user_limits = {}
        logger.info("Rate limits reset")
# Rate limit settings per action type
        self.limits = {
            'conversation': {'requests': 15, 'window': 60},   # 15 requests per minute
            'command': {'requests': 25, 'window': 60},        # 25 commands per minute
            'image': {'requests': 5, 'window': 300},          # 5 images per 5 minutes
            'api': {'requests': 30, 'window': 60},            # 30 API calls per minute
            'follow_up': {'requests': 3, 'window': 300}       # 3 follow-ups per 5 minutes
        }