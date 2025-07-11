import discord
from discord.ext import commands
import asyncio
import logging
import os
import random
import re
import hashlib
import time
from config import Config
from database import Database
from api_client import APIClient
from commands import BotCommands
from personality import PersonalityManager
from rate_limiter import RateLimiter
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedDiscordBot(commands.Bot):
    def __init__(self):
        # Set up intents to read all messages
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(command_prefix='!', intents=intents, help_command=None)
        
        # Track startup time
        self.start_time = datetime.now()
        
        # Initialize components
        self.config = Config()
        self.db = Database()
        self.api_client = APIClient()
        self.personality = PersonalityManager()
        self.rate_limiter = RateLimiter(self.db)
        
        # Bot settings - configurable via !config
        self.settings = self.config.get_bot_settings()
        
        # Security settings
        self.security = self.config.get_security_settings()
        self.security['trusted_users'] = set()  # Add user IDs here for trusted users
        
        # Bot names that will trigger responses
        self.bot_names = [
            'bilota', 'billota', 'kaala', 'kaala billota', 'bot', 'ai', 'assistant'
        ]
        
        # Add commands
        self.bot_commands = BotCommands(self)
        
        # Message tracking for anti-spam
        self.message_history = {}
        
    def is_trusted_user(self, user_id: str) -> bool:
        """Check if user is trusted (bypasses some restrictions)"""
        return str(user_id) in self.security['trusted_users']
        
    def check_message_security(self, message_content: str, user_id: str) -> tuple[bool, str]:
        """Check message for security issues"""
        # Check for blocked words
        content_lower = message_content.lower()
        for word in self.security['blocked_words']:
            if word in content_lower:
                return False, f"Message contains blocked word: {word}"
        
        # Check message length
        if len(message_content) > self.security['max_message_length']:
            return False, "Message too long"
            
        # Anti-spam check
        if self.security['anti_spam_enabled']:
            current_time = time.time()
            if user_id not in self.message_history:
                self.message_history[user_id] = []
            
            # Remove old messages (older than 10 seconds)
            self.message_history[user_id] = [
                msg_time for msg_time in self.message_history[user_id] 
                if current_time - msg_time < 10
            ]
            
            # Check if too many messages in short time
            if len(self.message_history[user_id]) >= 5:
                return False, "Too many messages in short time"
            
            self.message_history[user_id].append(current_time)
        
        return True, "OK"
    
    def replace_mentions_with_names(self, message_content, guild):
        """Replace Discord mention tags with display names"""
        if not guild:
            return message_content
            
        def repl(match):
            user_id = int(match.group(1))
            member = guild.get_member(user_id)
            return f"@{member.display_name}" if member else "@someone"
        return re.sub(r"<@!?(\d+)>", repl, message_content)
    
    def is_name_mentioned(self, message_content):
        """Check if bot's name is mentioned in the message"""
        content_lower = message_content.lower()
        return any(name in content_lower for name in self.bot_names)
        
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'{self.user} has connected to Discord! 🎉')
        await self.change_presence(activity=discord.Game(name="Chatting with friends! Type !config"))
        
    async def on_message(self, message):
        """Handle all messages - respond naturally, not just to commands"""
        # Don't respond to self
        if message.author == self.user:
            return
            
        # Security check
        security_ok, security_msg = self.check_message_security(
            message.content, 
            str(message.author.id)
        )
        
        if not security_ok and not self.is_trusted_user(message.author.id):
            logger.warning(f"Security check failed for {message.author}: {security_msg}")
            return
            
        # Process commands first
        await self.process_commands(message)
        
        # If it's not a command, respond naturally
        if not message.content.startswith('!'):
            await self.handle_natural_conversation(message)
    
    async def handle_natural_conversation(self, message):
        """Handle natural conversation for all non-command messages"""
        try:
            user_id = str(message.author.id)
            
            # Check if bot is mentioned, DM, or name is called
            is_mentioned = self.user in message.mentions
            is_dm = isinstance(message.channel, discord.DMChannel)
            is_name_called = self.is_name_mentioned(message.content)
            
            # Determine if we should respond
            should_respond = False
            if is_mentioned or is_dm or is_name_called:
                should_respond = True
            elif self.settings['random_chat_enabled'] and random.random() < self.settings['chat_frequency']:
                should_respond = True
                
            if not should_respond:
                return
                
            # Check rate limits
            if not self.rate_limiter.check_limit(user_id, 'conversation'):
                await message.add_reaction('⏰')
                return
                
            # Get user data
            user_data = self.db.get_user(user_id)
            
            # Clean message content - replace mentions with names
            clean_content = self.replace_mentions_with_names(message.content, message.guild)
            
            # --- Personality mode selection logic ---
            user_personality_mode = self.db.get_personality_mode(user_id)
            if user_personality_mode and user_personality_mode != 'friendly':
                personality_mode = user_personality_mode
            else:
                personality_mode = self.settings['personality_mode']
            # --------------------------------------
            
            # Generate natural response using personality with custom prompt support
            async with message.channel.typing():
                response = self.personality.generate_response(
                    clean_content, 
                    message.author.display_name,
                    personality_mode,
                    self.db.get_conversation_history(user_id),
                    self.api_client,
                    user_id,
                    str(message.guild.id) if message.guild else None
                )
                
                if response:
                    # Save conversation
                    self.db.add_conversation(user_id, clean_content, response)
                    
                    # Send response as normal text
                    sent_message = await message.reply(response)
                    
                    # Add random reactions if enabled
                    if self.settings['reactions_enabled']:
                        reactions = ['😊', '👍', '🎉', '💫', '✨', '🤔', '😄']
                        await sent_message.add_reaction(random.choice(reactions))
                    
        except Exception as e:
            logger.error(f"Error in natural conversation: {e}")
            await message.add_reaction('❌')

    def update_settings(self, new_settings: dict):
        """Update bot settings and sync with configuration"""
        self.settings.update(new_settings)
        self.config.update_bot_settings(new_settings)
        logger.info(f"Settings updated: {list(new_settings.keys())}")
    
    def update_security_settings(self, new_settings: dict):
        """Update security settings and sync with configuration"""
        self.security.update(new_settings)
        self.config.update_security_settings(new_settings)
        logger.info(f"Security settings updated: {list(new_settings.keys())}")
    
    def reload_config(self):
        """Reload configuration from file"""
        self.config.load_config()
        self.settings = self.config.get_bot_settings()
        self.security = self.config.get_security_settings()
        self.security['trusted_users'] = set()  # Preserve trusted users
        logger.info("Configuration reloaded")

async def setup_bot():
    """Set up and run the bot"""
    bot = AdvancedDiscordBot()
    
    # Add all commands (await required in modern discord.py)
    await bot.add_cog(bot.bot_commands)
    
    # Load config commands
    try:
        await bot.load_extension('config_commands')
        logger.info("Loaded config commands")
    except Exception as e:
        logger.error(f"Failed to load config commands: {e}")
    
    # Load custom prompt commands
    try:
        await bot.load_extension('custom_prompt_commands')
        logger.info("Loaded custom prompt commands")
    except Exception as e:
        logger.error(f"Failed to load custom prompt commands: {e}")
    
    # Get bot token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable not set!")
        exit(1)
        
    # Run the bot
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(setup_bot())
