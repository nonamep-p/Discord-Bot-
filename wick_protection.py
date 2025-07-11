import discord
import random
import time
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class WickProtection:
    """Protection system to avoid Wick bot detection"""
    
    def __init__(self):
        self.message_patterns = []
        self.response_delays = []
        self.typing_patterns = []
        self.last_message_time = {}
        
    def add_human_delay(self, channel_id: str) -> float:
        """Add random human-like delay before responding"""
        # Random delay between 1-5 seconds
        delay = random.uniform(1.0, 5.0)
        time.sleep(delay)
        return delay
    
    def simulate_typing(self, channel, duration: float = None):
        """Simulate human typing behavior"""
        if duration is None:
            duration = random.uniform(2.0, 8.0)
        
        # Start typing indicator
        typing_task = channel.trigger_typing()
        
        # Stop typing after duration
        time.sleep(duration)
        typing_task.cancel()
    
    def vary_response_length(self, response: str) -> str:
        """Vary response length to seem more human"""
        # Sometimes add extra context or emojis
        if random.random() < 0.3:
            emojis = ['😊', '👍', '🎉', '💫', '✨', '🤔', '😄', '👋', '💯']
            response += f" {random.choice(emojis)}"
        
        return response
    
    def avoid_patterns(self, response: str) -> str:
        """Avoid common bot patterns that Wick might detect"""
        # Don't always start with the same words
        bot_starters = [
            "I think", "Well", "That's", "You're", "It's", "I'm", "Let me"
        ]
        
        if any(response.startswith(starter) for starter in bot_starters):
            # Add variety
            starters = [
                "Hmm", "Oh", "Hey", "Yeah", "Right", "True", "Good point"
            ]
            response = f"{random.choice(starters)}, {response.lower()}"
        
        return response
    
    def get_safe_response_style(self) -> Dict:
        """Get response style that avoids detection"""
        return {
            'use_typing': random.random() < 0.8,  # 80% chance to use typing
            'delay_before_response': random.uniform(1.0, 4.0),
            'add_emojis': random.random() < 0.4,
            'vary_length': random.random() < 0.6
        }
    
    def is_safe_to_respond(self, channel_id: str, user_id: str) -> bool:
        """Check if it's safe to respond without triggering Wick"""
        current_time = time.time()
        
        # Don't respond too frequently
        if channel_id in self.last_message_time:
            time_since_last = current_time - self.last_message_time[channel_id]
            if time_since_last < 30:  # Minimum 30 seconds between responses
                return False
        
        self.last_message_time[channel_id] = current_time
        return True

class HumanLikeResponder:
    """Makes bot responses more human-like to avoid detection"""
    
    def __init__(self):
        self.wick_protection = WickProtection()
        
    async def send_human_response(self, channel, response: str, user_id: str = None):
        """Send response in a human-like way"""
        # Get safe response style
        style = self.wick_protection.get_safe_response_style()
        
        # Check if safe to respond
        if not self.wick_protection.is_safe_to_respond(str(channel.id), str(user_id) if user_id else "unknown"):
            return None
        
        # Add human-like delay
        await asyncio.sleep(style['delay_before_response'])
        
        # Use typing indicator
        if style['use_typing']:
            async with channel.typing():
                await asyncio.sleep(random.uniform(1.0, 3.0))
        
        # Vary response
        response = self.wick_protection.vary_response_length(response)
        response = self.wick_protection.avoid_patterns(response)
        
        return response
