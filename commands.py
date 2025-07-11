import discord
from discord.ext import commands
import asyncio
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class BotCommands(commands.Cog):
    """All bot commands"""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show all available commands"""
        embed = discord.Embed(
            title="🤖 Bot Commands & Features",
            description="Here's everything I can do! I also respond to normal messages naturally 😊",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="💬 Chat Commands",
            value="""
            `!chat [message]` - Direct AI chat (10 coins)
            `!roleplay [character]` - Switch personality mode
            """,
            inline=False
        )
        
        embed.add_field(
            name="🎨 Fun Commands", 
            value="""
            `!image [prompt]` - Generate image (50 coins)
            `!gif [search]` - Find GIF (5 coins)
            """,
            inline=False
        )
        
        embed.add_field(
            name="💰 Economy Commands",
            value="""
            `!balance` - Check your coins
            `!daily` - Get daily coins (100 coins)
            `!gift [user] [amount]` - Give coins to someone
            """,
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ Info Commands",
            value="""
            `!limits` - Show remaining API limits
            `!ping` - Check bot status
            `!help` - Show this message
            """,
            inline=False
        )
        
        embed.add_field(
            name="✨ Special Features",
            value="""
            • I respond to ALL messages naturally!
            • Mention me or DM me for conversations
            • I remember our chat history
            • I can roleplay different characters
            • I add reactions and use emojis
            """,
            inline=False
        )
        
        embed.set_footer(text="💡 Tip: I respond to normal messages too, not just commands!")
        await ctx.send(embed=embed)
        
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot status and latency"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot is online and responsive!\n**Latency:** {latency}ms",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('🏓')
        
    @commands.command(name='balance')
    async def balance(self, ctx):
        """Check user's coin balance"""
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        embed = discord.Embed(
            title="💰 Your Balance",
            description=f"**{user_data['coins']}** coins",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Stats",
            value=f"Commands used: {user_data.get('total_commands', 0)}",
            inline=True
        )
        
        embed.set_footer(text="Use !daily to get 100 coins daily!")
        await ctx.send(embed=embed)
        
    @commands.command(name='daily')
    async def daily(self, ctx):
        """Claim daily coin reward"""
        user_id = str(ctx.author.id)
        
        if self.bot.db.can_claim_daily(user_id):
            new_balance = self.bot.db.claim_daily(user_id)
            
            embed = discord.Embed(
                title="🎁 Daily Reward Claimed!",
                description=f"You received **100 coins**!\nNew balance: **{new_balance}** coins",
                color=discord.Color.green()
            )
            
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('🎉')
        else:
            embed = discord.Embed(
                title="⏰ Daily Reward Already Claimed",
                description="You've already claimed your daily reward today!\nCome back tomorrow for more coins.",
                color=discord.Color.orange()
            )
            
            await ctx.send(embed=embed)
            
    @commands.command(name='gift')
    async def gift(self, ctx, user: discord.Member = None, amount: int = None):
        """Gift coins to another user"""
        if not user or not amount:
            embed = discord.Embed(
                title="❌ Invalid Usage",
                description="Usage: `!gift @user amount`\nExample: `!gift @friend 50`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
            
        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
            
        if user == ctx.author:
            await ctx.send("❌ You can't gift coins to yourself!")
            return
            
        sender_id = str(ctx.author.id)
        receiver_id = str(user.id)
        
        if self.bot.db.transfer_coins(sender_id, receiver_id, amount):
            embed = discord.Embed(
                title="🎁 Coins Gifted!",
                description=f"{ctx.author.mention} gifted **{amount} coins** to {user.mention}!",
                color=discord.Color.green()
            )
            
            sender_balance = self.bot.db.get_user(sender_id)['coins']
            embed.add_field(name="Your new balance", value=f"{sender_balance} coins", inline=True)
            
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('💝')
        else:
            await ctx.send("❌ You don't have enough coins for this gift!")
            
    @commands.command(name='chat')
    async def chat(self, ctx, *, message: str = None):
        """Direct AI chat"""
        if not message:
            await ctx.send("❌ Please provide a message to chat about!")
            return
            
        user_id = str(ctx.author.id)
        
        # Check rate limits
        if not self.bot.rate_limiter.check_limit(user_id, 'api_calls'):
            await ctx.send("⏰ You've hit your hourly API limit! Try again later.")
            return
            
        # Check and spend coins
        if not self.bot.db.spend_coins(user_id, 10):
            await ctx.send("❌ You need 10 coins to use this command! Use `!daily` to get more.")
            return
            
        async with ctx.typing():
            # Get conversation history
            history = self.bot.db.get_conversation_history(user_id)
            user_data = self.bot.db.get_user(user_id)
            
            # Generate response
            response = await self.bot.personality.generate_response(
                message,
                ctx.author.display_name,
                user_data.get('personality_mode', 'default'),
                history,
                self.bot.api_client
            )
            
            if response:
                # Update usage
                self.bot.db.update_usage(user_id, 'api_call')
                self.bot.db.add_conversation(user_id, message, response)
                
                # Send as plain text with a simple indicator
                await ctx.send(f"{response}\n\n💬 *Chat response • 10 coins spent*")
            else:
                await ctx.send("❌ Sorry, I couldn't generate a response right now!")
                # Refund coins on failure
                self.bot.db.add_coins(user_id, 10)
                
    @commands.command(name='roleplay')
    async def roleplay(self, ctx, *, character: str = None):
        """Switch to roleplay mode"""
        if not character:
            embed = discord.Embed(
                title="🎭 Roleplay Mode",
                description="Usage: `!roleplay [character]`\n\nExamples:\n• `!roleplay pirate`\n• `!roleplay wise wizard`\n• `!roleplay friendly cat`\n• `!roleplay default` (reset)",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            return
            
        user_id = str(ctx.author.id)
        
        # Set personality mode
        self.bot.db.set_personality_mode(user_id, character.lower())
        
        embed = discord.Embed(
            title="🎭 Roleplay Mode Activated!",
            description=f"I'm now roleplaying as: **{character}**\n\nI'll respond as this character in our conversations!",
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('🎭')
        
    @commands.command(name='gif')
    async def gif(self, ctx, *, search_term: str = None):
        """Search for a GIF"""
        if not search_term:
            await ctx.send("❌ Please provide a search term for the GIF!")
            return
            
        user_id = str(ctx.author.id)
        
        # Check and spend coins
        if not self.bot.db.spend_coins(user_id, 5):
            await ctx.send("❌ You need 5 coins to use this command!")
            return
            
        async with ctx.typing():
            gif_url = await self.bot.api_client.search_gif(search_term)
            
            if gif_url:
                embed = discord.Embed(
                    title=f"🎬 GIF: {search_term}",
                    color=discord.Color.green()
                )
                embed.set_image(url=gif_url)
                embed.set_footer(text="🎬 GIF • 5 coins spent")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Couldn't find a GIF for '{search_term}'!")
                # Refund coins on failure
                self.bot.db.add_coins(user_id, 5)
                
    @commands.command(name='image')
    async def image(self, ctx, *, prompt: str = None):
        """Generate an image"""
        if not prompt:
            await ctx.send("❌ Please provide a prompt for image generation!")
            return
            
        user_id = str(ctx.author.id)
        
        # Check rate limits
        usage_data = self.bot.db.get_usage_data(user_id)
        if usage_data.get('images_today', 0) >= 10:
            await ctx.send("⏰ You've hit your daily image limit (10)! Try again tomorrow.")
            return
            
        # Check and spend coins
        if not self.bot.db.spend_coins(user_id, 50):
            await ctx.send("❌ You need 50 coins to use this command!")
            return
            
        async with ctx.typing():
            result = await self.bot.api_client.generate_image(prompt)
            
            if result:
                # Update usage
                self.bot.db.update_usage(user_id, 'image')
                
                embed = discord.Embed(
                    title=f"🎨 Generated Image",
                    description=f"**Prompt:** {prompt}\n\n{result}",
                    color=discord.Color.orange()
                )
                embed.set_footer(text="🎨 Image Generation • 50 coins spent")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Couldn't generate image right now!")
                # Refund coins on failure
                self.bot.db.add_coins(user_id, 50)
                
    @commands.command(name='limits')
    async def limits(self, ctx):
        """Show remaining API limits"""
        user_id = str(ctx.author.id)
        usage_data = self.bot.db.get_usage_data(user_id)
        
        api_calls_remaining = max(0, 50 - usage_data.get('hourly_calls', 0))
        images_remaining = max(0, 10 - usage_data.get('images_today', 0))
        
        embed = discord.Embed(
            title="📊 Your Usage Limits",
            description="Here are your remaining limits for today:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🔄 API Calls (Hourly)",
            value=f"{api_calls_remaining}/50 remaining",
            inline=True
        )
        
        embed.add_field(
            name="🎨 Images (Daily)", 
            value=f"{images_remaining}/10 remaining",
            inline=True
        )
        
        embed.add_field(
            name="📅 Reset Times",
            value="• API calls: Every hour\n• Images: Daily at midnight",
            inline=False
        )
        
        await ctx.send(embed=embed)
