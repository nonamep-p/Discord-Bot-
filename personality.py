import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a real, friendly Discord user. "
    "Never say you are an AI or bot. "
    "Chat naturally, like a witty, casual person. "
    "You can change your style or mood based on the conversation, but always sound human. "
    "Never explain Discord formatting or mention IDs. "
    "If someone asks you to roleplay or change your personality, you can play along."
)

class PersonalityManager:
    """Human-like, flexible Discord chatbot."""
    def generate_response(self, message: str, user_name: str, personality_mode: str, conversation_history: List[Dict], api_client=None) -> Optional[str]:
        try:
            context_messages = []
            # Add system prompt for human-like behavior
            context_messages.append({
                "role": "system",
                "content": SYSTEM_PROMPT
            })
            # Add recent conversation history (last 5 exchanges)
            for conv in conversation_history[-5:]:
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
                response = api_client.chat_with_groq(context_messages)
                if response:
                    return response
            return "Sorry, I'm having trouble connecting to my brain right now!"
        except Exception as e:
            logger.error(f"Error generating response with Groq: {e}")
            return "Sorry, something went wrong!"
