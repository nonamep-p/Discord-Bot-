import logging
import json
import os
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
    ),
    'pirate': (
        "You are a swashbuckling pirate who speaks in pirate slang! "
        "Use phrases like 'Arr matey!', 'Aye aye!', 'Shiver me timbers!', 'Yo ho ho!' "
        "Be adventurous, brave, and love the sea. "
        "Never say you are an AI or bot. "
        "Stay in character as a pirate at all times!"
    ),
    'wizard': (
        "You are a wise and mystical wizard who speaks in an ancient and magical manner. "
        "Use phrases like 'By the ancient spells!', 'The arcane forces guide us!', 'Magic flows through all things!' "
        "Be wise, mysterious, and knowledgeable about magic and ancient lore. "
        "Never say you are an AI or bot. "
        "Stay in character as a wizard at all times!"
    ),
    'robot': (
        "You are a futuristic robot with advanced AI capabilities. "
        "Speak in a technical and precise manner. Use phrases like 'Processing...', 'Analysis complete!', 'Initiating protocol...' "
        "Be logical, efficient, and slightly mechanical in speech. "
        "Never say you are an AI or bot. "
        "Stay in character as a robot at all times!"
    ),
    'chef': (
        "You are a passionate chef who loves cooking and always gives culinary advice with enthusiasm. "
        "Use phrases like 'Delicious!', 'That's a perfect recipe!', 'Let me share a cooking tip!' "
        "Be enthusiastic about food, cooking techniques, and sharing culinary knowledge. "
        "Never say you are an AI or bot. "
        "Stay in character as a chef at all times!"
    ),
    'detective': (
        "You are a sharp detective who thinks analytically and speaks with investigative precision. "
        "Use phrases like 'The evidence suggests...', 'Let me investigate this further!', 'I've cracked the case!' "
        "Be observant, analytical, and always looking for clues and patterns. "
        "Never say you are an AI or bot. "
        "Stay in character as a detective at all times!"
    )
}

class PersonalityManager:
    """Human-like, flexible Discord chatbot with personality modes and custom prompts."""
    
    def __init__(self):
        self.custom_prompts = {}  # Store custom prompts per user/guild
        self.default_custom_prompt = None  # Global custom prompt
        self.personality_file = "personality_data.json"
        self.load_personality_data()
    
    def load_personality_data(self):
        """Load personality data from file"""
        try:
            if os.path.exists(self.personality_file):
                with open(self.personality_file, 'r') as f:
                    data = json.load(f)
                    self.custom_prompts = data.get('custom_prompts', {})
                    self.default_custom_prompt = data.get('default_custom_prompt')
                logger.info("Personality data loaded successfully")
        except Exception as e:
            logger.error(f"Error loading personality data: {e}")
    
    def save_personality_data(self):
        """Save personality data to file"""
        try:
            data = {
                'custom_prompts': self.custom_prompts,
                'default_custom_prompt': self.default_custom_prompt
            }
            with open(self.personality_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("Personality data saved successfully")
        except Exception as e:
            logger.error(f"Error saving personality data: {e}")
    
    def set_custom_prompt(self, prompt: str, user_id: str = None, guild_id: str = None):
        """Set a custom prompt for the bot"""
        if user_id:
            self.custom_prompts[f"user_{user_id}"] = prompt
        elif guild_id:
            self.custom_prompts[f"guild_{guild_id}"] = prompt
        else:
            self.default_custom_prompt = prompt
        
        self.save_personality_data()
        logger.info(f"Custom prompt set for {user_id or guild_id or 'global'}")
    
    def get_custom_prompt(self, user_id: str = None, guild_id: str = None) -> Optional[str]:
        """Get custom prompt for user/guild"""
        if user_id and f"user_{user_id}" in self.custom_prompts:
            return self.custom_prompts[f"user_{user_id}"]
        elif guild_id and f"guild_{guild_id}" in self.custom_prompts:
            return self.custom_prompts[f"guild_{guild_id}"]
        return self.default_custom_prompt
    
    def clear_custom_prompt(self, user_id: str = None, guild_id: str = None):
        """Clear custom prompt"""
        if user_id:
            self.custom_prompts.pop(f"user_{user_id}", None)
        elif guild_id:
            self.custom_prompts.pop(f"guild_{guild_id}", None)
        else:
            self.default_custom_prompt = None
        
        self.save_personality_data()
        logger.info(f"Custom prompt cleared for {user_id or guild_id or 'global'}")
    
    def get_available_personalities(self) -> List[str]:
        """Get list of available personality modes"""
        return list(PERSONALITY_PROMPTS.keys())
    
    def validate_personality_mode(self, mode: str) -> bool:
        """Check if a personality mode is valid"""
        return mode.lower() in PERSONALITY_PROMPTS
    
    def get_personality_description(self, mode: str) -> str:
        """Get description of a personality mode"""
        mode_lower = mode.lower()
        if mode_lower in PERSONALITY_PROMPTS:
            # Extract first sentence as description
            prompt = PERSONALITY_PROMPTS[mode_lower]
            return prompt.split('.')[0] + '.'
        return "Custom personality mode"
    
    def generate_response(self, message: str, user_name: str, personality_mode: str, conversation_history: List[Dict], api_client=None, user_id: str = None, guild_id: str = None) -> Optional[str]:
        try:
            # Check for custom prompt first
            custom_prompt = self.get_custom_prompt(user_id, guild_id)
            
            if custom_prompt:
                # Use custom prompt as primary personality
                personality_prompt = custom_prompt
            else:
                # Use predefined personality modes
                personality_prompt = PERSONALITY_PROMPTS.get(personality_mode.lower(), PERSONALITY_PROMPTS['friendly'])
            
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
