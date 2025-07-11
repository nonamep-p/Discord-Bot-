import discord
from discord.ext import commands
import asyncio
import logging
import os
from config import Config
from database import Database
from api_client import APIClient
from commands import BotCommands
from personality import PersonalityManager
from rate_limiter import RateLimiter

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
        
        # Initialize components
        self.config = Config()
        self.db = Database()
        self.api_client = APIClient()
        self.personality = PersonalityManager()
        self.rate_limiter = RateLimiter()
        
        # Add commands
        self.bot_commands = BotCommands(self)
        
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'{self.user} has connected to Discord! 🎉')
        await self.change_presence(activity=discord.Game(name="Being awesome! Type !help"))
        
    async def on_message(self, message):
        """Handle all messages - respond naturally, not just to commands"""
        # Don't respond to self
        if message.author == self.user:
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
            
            # Check if bot is mentioned or DM
            is_mentioned = self.user in message.mentions
            is_dm = isinstance(message.channel, discord.DMChannel)
            
            # Only respond if mentioned, DM, or randomly (10% chance)
            import random
            should_respond = is_mentioned or is_dm or random.random() < 0.1
            
            if not should_respond:
                return
                
            # Check rate limits
            if not self.rate_limiter.check_limit(user_id, 'conversation'):
                await message.add_reaction('⏰')
                return
                
            # Get user data and ensure they have coins
            user_data = self.db.get_user(user_id)
            
            # Generate natural response using personality
            async with message.channel.typing():
                response = await self.personality.generate_response(
                    message.content, 
                    message.author.display_name,
                    user_data.get('personality_mode', 'default'),
                    self.db.get_conversation_history(user_id),
                    self.api_client
                )
                
                if response:
                    # Save conversation
                    self.db.add_conversation(user_id, message.content, response)
                    
                    # Send response as normal text
                    sent_message = await message.reply(response)
                    
                    # Add random reactions
                    reactions = ['😊', '👍', '🎉', '💫', '✨']
                    await sent_message.add_reaction(random.choice(reactions))
                    
        except Exception as e:
            logger.error(f"Error in natural conversation: {e}")
            await message.add_reaction('❌')

async def setup_bot():
    """Set up and run the bot"""
    bot = AdvancedDiscordBot()
    
    # Add all commands (await required in modern discord.py)
    await bot.add_cog(bot.bot_commands)
    
    # Get bot token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("DISCORD_BOT_TOKEN environment variable not set!")
        exit(1)
        
    # Run the bot
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(setup_bot())
