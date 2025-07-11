import aiohttp
import asyncio
import json
import logging
from typing import Optional, Dict, List
import os

logger = logging.getLogger(__name__)

class APIClient:
    """Handle external API calls"""
    
    def __init__(self):
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY', 'default_deepseek_key')
        self.giphy_api_key = os.getenv('GIPHY_API_KEY', 'default_giphy_key')
        self.deepseek_url = 'https://api.deepseek.com/v1/chat/completions'
        self.giphy_url = 'https://api.giphy.com/v1/gifs/search'
        
    async def chat_with_deepseek(self, messages: List[Dict], personality_prompt: str = "") -> Optional[str]:
        """Send chat request to Deepseek API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Prepare messages with personality
            system_message = {
                "role": "system",
                "content": f"""You are a friendly Discord bot with personality. {personality_prompt}
                
Key traits:
- Act like a real person, not a formal assistant
- Use casual, friendly language with emojis
- Be funny, helpful, and slightly sarcastic
- Keep responses conversational and engaging
- Remember you're chatting in Discord
- Keep responses under 1500 characters
- Use emojis naturally but don't overdo it"""
            }
            
            full_messages = [system_message] + messages
            
            payload = {
                'model': 'deepseek-chat',
                'messages': full_messages,
                'max_tokens': 300,
                'temperature': 0.8,
                'stream': False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.deepseek_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        response_text = await response.text()
                        logger.error(f"Deepseek API error: {response.status} - {response_text}")
                        # Check if it's an authentication error
                        if response.status == 401:
                            logger.warning("Deepseek API authentication failed - check DEEPSEEK_API_KEY")
                        return None
                        
        except Exception as e:
            logger.error(f"Error calling Deepseek API: {e}")
            return None
            
    async def search_gif(self, query: str, limit: int = 1) -> Optional[str]:
        """Search for GIF using Giphy API"""
        try:
            params = {
                'api_key': self.giphy_api_key,
                'q': query,
                'limit': limit,
                'rating': 'pg-13',
                'lang': 'en'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.giphy_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['data']:
                            return data['data'][0]['images']['original']['url']
                        return None
                    else:
                        logger.error(f"Giphy API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error calling Giphy API: {e}")
            return None
            
    async def generate_image(self, prompt: str) -> Optional[str]:
        """Generate image using AI (placeholder - would integrate with actual image API)"""
        # This would integrate with actual image generation API like DALL-E, Midjourney, etc.
        # For now, return a placeholder response
        try:
            # In a real implementation, you would call an image generation API here
            logger.info(f"Image generation requested for: {prompt}")
            return f"🎨 Image generation for '{prompt}' would happen here! (Not implemented with real API yet)"
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None
