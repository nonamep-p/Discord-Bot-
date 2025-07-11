import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class PersonalityManager:
    """Pure Groq-powered chatbot. No templates, no personas."""
    async def generate_response(self, message: str, user_name: str, personality_mode: str, conversation_history: List[Dict], api_client=None) -> Optional[str]:
        try:
            context_messages = []
            for conv in conversation_history[-3:]:
                context_messages.append({
                    "role": "user",
                    "content": conv['user_message']
                })
                context_messages.append({
                    "role": "assistant",
                    "content": conv['bot_response']
                })
            context_messages.append({
                "role": "user",
                "content": f"{user_name} says: {message}"
            })
            if api_client:
                response = await api_client.chat_with_groq(context_messages)
                if response:
                    return response
            return "Sorry, I'm having trouble connecting to my brain right now!"
        except Exception as e:
            logger.error(f"Error generating response with Groq: {e}")
            return "Sorry, something went wrong!"
