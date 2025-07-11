import openai
import os
import logging
from typing import Optional, Dict, List
import requests

logger = logging.getLogger(__name__)

class APIClient:
    """Handle external API calls using Groq Llama-3"""
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            logger.error("GROQ_API_KEY environment variable not set!")
        openai.api_key = self.groq_api_key
        openai.base_url = "https://api.groq.com/openai/v1/"

    def chat_with_groq(self, messages: List[Dict], personality_prompt: str = "") -> Optional[str]:
        try:
            if not self.groq_api_key:
                return "Sorry, I'm not configured to chat right now."
                
            chat_messages = []
            if personality_prompt:
                chat_messages.append({"role": "system", "content": personality_prompt})
            chat_messages.extend(messages)
            
            response = openai.chat.completions.create(
                model="llama3-70b-8192",
                messages=chat_messages,
                max_tokens=1024,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return None

    async def search_gif(self, query: str, limit: int = 1) -> Optional[str]:
        """Search for a GIF using the GIPHY API and return the URL of the first result."""
        giphy_api_key = os.getenv('GIPHY_API_KEY')
        if not giphy_api_key:
            logger.error("GIPHY_API_KEY environment variable not set!")
            return None
        try:
            url = f"https://api.giphy.com/v1/gifs/search"
            params = {
                'api_key': giphy_api_key,
                'q': query,
                'limit': limit,
                'rating': 'pg',
                'lang': 'en'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data['data']:
                return data['data'][0]['images']['original']['url']
            else:
                return None
        except Exception as e:
            logger.error(f"Error searching GIF: {e}")
            return None

    async def generate_image(self, prompt: str) -> Optional[str]:
        # Groq does not support image generation
        return "Image generation is not supported on the free Groq API."
