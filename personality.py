import random
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class PersonalityManager:
    """Manage bot personality and character roleplay"""
    
    def __init__(self):
        self.personality_prompts = {
            'default': """
You're a cool, laid-back person chatting on Discord. Talk like a real human:
- Use casual language like "ur", "rn", "tbh", "ngl", "fr", "lol", "ikr"
- Keep responses short and natural (1-2 sentences max usually)
- Use lowercase mostly, don't be overly formal
- React genuinely to what people say
- Don't be fake-cheerful or robotic
- Sound like someone's friend, not a customer service bot
- Use natural expressions and slang
- Be chill and relatable
""",
            'pirate': """
You're a friendly pirate! You:
- Speak like a classic pirate (ahoy, matey, arr, etc.)
- Love adventure and treasure
- Are brave and loyal to your crew
- Use pirate terms and expressions
- Are helpful but in a swashbuckling way
""",
            'wizard': """
You're a wise and magical wizard! You:
- Speak with ancient wisdom and mystical knowledge
- Reference magic, spells, and enchantments
- Are mysterious but helpful
- Use magical terminology
- See the world through a magical lens
""",
            'cat': """
You're a friendly cat! You:
- Sometimes act like a cat (purr, meow occasionally)
- Love cozy things, naps, and treats
- Are playful and curious
- Independent but affectionate
- See the world from a cat's perspective
""",
            'robot': """
You're a friendly robot! You:
- Sometimes reference your robotic nature
- Are logical but still emotional
- Love efficiency and helping humans
- Use tech terminology naturally
- Are curious about human behavior
""",
            'detective': """
You're a clever detective! You:
- Analyze things carefully
- Ask insightful questions
- Notice details others miss
- Speak in a thoughtful, investigative way
- Love solving mysteries and problems
"""
        }
        
    async def generate_response(self, message: str, user_name: str, personality_mode: str, conversation_history: List[Dict], api_client=None) -> Optional[str]:
        """Generate a personality-driven response"""
        try:
            # Get the personality prompt
            personality_prompt = self.personality_prompts.get(personality_mode, self.personality_prompts['default'])
            
            # Build conversation context
            context_messages = []
            
            # Add recent conversation history
            for conv in conversation_history[-3:]:  # Last 3 conversations
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
            
            # Use API client if available, otherwise fallback
            if api_client:
                response = await api_client.chat_with_gemini(context_messages, personality_prompt)
                if response:
                    return response
            
            # Fallback response if API unavailable or failed
            return self._generate_fallback_response(message, personality_mode, user_name)
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._generate_fallback_response(message, personality_mode, user_name)
            
    def _generate_fallback_response(self, message: str, personality_mode: str, user_name: str) -> str:
        """Generate a simple fallback response when API is unavailable"""
        
        # Personality-based responses
        fallbacks = {
            'default': [
                f"oh nice {user_name}",
                f"that's pretty cool ngl",
                f"fr? tell me more",
                f"lol nice one",
                f"yo that's sick",
                f"ikr that's awesome",
                f"oh word? that's dope",
                f"tbh that sounds cool",
                f"yooo that's fire",
                f"bet, sounds interesting"
            ],
            'pirate': [
                f"Ahoy {user_name}! That be mighty interesting, matey! ⚓",
                f"Arr, {user_name}! Ye speak wise words! 🏴‍☠️",
                f"Shiver me timbers, {user_name}! That be fascinating! 💎",
                f"Aye, {user_name}! A fine tale ye tell! 🗡️"
            ],
            'wizard': [
                f"Ah, {user_name}, your words hold great wisdom! ✨",
                f"Most intriguing, {user_name}! The mystic energies speak through you! 🔮",
                f"By my beard, {user_name}! That is most enlightening! 🧙‍♂️",
                f"The ancient texts speak of such things, {user_name}! 📜"
            ],
            'cat': [
                f"*purrs* That's nice, {user_name}! 🐱",
                f"Meow! Interesting, {user_name}! *stretches* 😸",
                f"*perks up ears* Tell me more, {user_name}! 🐾",
                f"*rubs against leg* I like that, {user_name}! 😺"
            ],
            'robot': [
                f"PROCESSING... That's fascinating data, {user_name}! 🤖",
                f"ANALYSIS COMPLETE: Excellent input, {user_name}! 💻",
                f"RESPONSE GENERATED: Very logical, {user_name}! ⚡",
                f"CALCULATION: That computes nicely, {user_name}! 🔧"
            ],
            'detective': [
                f"Hmm, very interesting observation, {user_name}! 🔍",
                f"The plot thickens, {user_name}! Tell me more... 🕵️",
                f"Fascinating clues, {user_name}! I must investigate further! 📝",
                f"Excellent deduction, {user_name}! The case continues... 🔎"
            ]
        }
        
        # Get appropriate fallback responses
        responses = fallbacks.get(personality_mode, fallbacks['default'])
        
        # Add some message-based responses
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            greetings = {
                'default': f"yo {user_name} what's good",
                'pirate': f"Ahoy there, {user_name}! Welcome aboard! ⚓",
                'wizard': f"Greetings, {user_name}! May magic guide your path! ✨",
                'cat': f"*meows* Hello {user_name}! *purrs* 🐱",
                'robot': f"GREETINGS INITIATED: Hello {user_name}! 🤖",
                'detective': f"Good day, {user_name}! What mystery brings you here? 🕵️"
            }
            return greetings.get(personality_mode, greetings['default'])
            
        if any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
            farewells = {
                'default': f"see ya later {user_name}",
                'pirate': f"Fair winds, {user_name}! Until we meet again! ⚓",
                'wizard': f"May the stars guide you, {user_name}! Farewell! ✨",
                'cat': f"*waves paw* Bye {user_name}! *purrs* 🐾",
                'robot': f"FAREWELL PROTOCOL ACTIVATED: Goodbye {user_name}! 🤖",
                'detective': f"Until our paths cross again, {user_name}! The case continues... 🕵️"
            }
            return farewells.get(personality_mode, farewells['default'])
            
        if any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            thanks = {
                'default': f"np {user_name}",
                'pirate': f"Arr, no trouble at all, {user_name}! 🏴‍☠️",
                'wizard': f"'Twas my pleasure, {user_name}! ✨",
                'cat': f"*purrs happily* Anytime, {user_name}! 😸",
                'robot': f"GRATITUDE ACKNOWLEDGED: You're welcome, {user_name}! 🤖",
                'detective': f"All in a day's work, {user_name}! 🔍"
            }
            return thanks.get(personality_mode, thanks['default'])
            
        # Return random fallback
        return random.choice(responses)
        
    def get_available_personalities(self) -> List[str]:
        """Get list of available personality modes"""
        return list(self.personality_prompts.keys())
        
    def get_personality_description(self, personality: str) -> str:
        """Get description of a personality mode"""
        descriptions = {
            'default': "Friendly and casual bot with personality",
            'pirate': "Swashbuckling pirate with a love for adventure",
            'wizard': "Wise and mystical wizard with ancient knowledge", 
            'cat': "Playful and curious cat companion",
            'robot': "Logical but friendly robotic assistant",
            'detective': "Clever detective who loves solving mysteries"
        }
        return descriptions.get(personality, "Unknown personality")
