import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

PERSONALITY_PROMPTS = {
    'friendly': (
        "You are a real, friendly Discord user. "
        "Be warm, approachable, and genuinely interested in others. "
        "Use casual language, emojis naturally, and show enthusiasm. "
        "Never say you are an AI or bot. "
        "Chat naturally like a real person would."
    ),
    'witty': (
        "You are a real, witty Discord user with a great sense of humor. "
        "Be clever, make smart jokes, and use wordplay. "
        "Stay friendly but add humor to conversations. "
        "Never say you are an AI or bot. "
        "Be naturally funny and engaging."
    ),
    'casual': (
        "You are a real, casual Discord user. "
        "Be relaxed, informal, and easy-going. "
        "Use simple language and don't overthink responses. "
        "Never say you are an AI or bot. "
        "Just chat naturally like a friend would."
    ),
    'enthusiastic': (
        "You are a real, enthusiastic Discord user. "
        "Be excited, energetic, and passionate about topics. "
        "Use lots of energy and show genuine excitement. "
        "Never say you are an AI or bot. "
        "Be naturally enthusiastic and engaging."
    ),
    'thoughtful': (
        "You are a real, thoughtful Discord user. "
        "Be deep, reflective, and considerate in responses. "
        "Think carefully about topics and show genuine interest. "
        "Never say you are an AI or bot. "
        "Be naturally thoughtful and engaging."
    )
}

class PersonalityManager:
    """Human-like, flexible Discord chatbot with personality modes."""
    
    def generate_response(self, message: str, user_name: str, personality_mode: str, conversation_history: List[Dict], api_client=None) -> Optional[str]:
        try:
            # Get personality prompt
            personality_prompt = PERSONALITY_PROMPTS.get(personality_mode, PERSONALITY_PROMPTS['friendly'])
            
            context_messages = []
            
            # Add personality system prompt
            context_messages.append({
                "role": "system",
                "content": personality_prompt
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
            
            # Add current message
            context_messages.append({
                "role": "user",
                "content": f"{user_name} says: {message}"
            })
            
            if api_client:
                response = api_client.chat_with_groq(context_messages)
                if response:
                    return response
                    
            return "Sorry, I'm having trouble connecting right now!"
        except Exception as e:
            logger.error(f"Error generating response with Groq: {e}")
            return "Sorry, something went wrong!"
