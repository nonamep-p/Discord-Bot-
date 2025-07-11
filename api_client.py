import aiohttp
import asyncio
import logging
from typing import Optional, Dict, List
import os
import google.generativeai as genai

logger = logging.getLogger(__name__)

class APIClient:
    """Handle external API calls (now using Gemini)"""
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.giphy_api_key = os.getenv('GIPHY_API_KEY', 'default_giphy_key')
        self.giphy_url = 'https://api.giphy.com/v1/gifs/search'
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
        else:
            logger.error("GEMINI_API_KEY not set!")

    async def chat_with_gemini(self, messages: List[Dict], personality_prompt: str = "") -> Optional[str]:
        """Send chat request to Gemini API"""
        try:
            # Gemini expects a single prompt string, so combine messages
            prompt = personality_prompt + "\n"
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    prompt += f"User: {content}\n"
                else:
                    prompt += f"Bot: {content}\n"
            prompt += "Bot:"
            model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
            response = await asyncio.to_thread(model.generate_content, prompt)
            return response.text.strip() if hasattr(response, 'text') else str(response)
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
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
        """Generate image using Gemini API (text fallback if vision not available)"""
        try:
            # If vision model is not available, fallback to text
            model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
            response = await asyncio.to_thread(model.generate_content, prompt)
            if hasattr(response, 'text'):
                return response.text.strip()
            return str(response)
        except Exception as e:
            logger.error(f"Error generating image with Gemini: {e}")
            return None
