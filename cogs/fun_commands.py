
import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.truth_questions = [
            "What's the most embarrassing thing you've done?",
            "Who was your first crush?",
            "What's your biggest fear?",
            "What's the weirdest dream you've had?",
            "What's your most used emoji?",
            "What's your guilty pleasure?",
            "What's the strangest food combination you enjoy?",
            "What's your biggest pet peeve?",
            "What's the last lie you told?",
            "What's your secret talent?"
        ]
        
        self.dare_challenges = [
            "Do 10 push-ups right now!",
            "Sing your favorite song in voice chat!",
            "Change your nickname to something silly for 1 hour",
            "Send a funny selfie in the chat",
            "Tell a joke that will make everyone laugh",
            "Speak in rhymes for the next 5 minutes",
            "Do an impression of your favorite celebrity",
            "Dance for 30 seconds in voice chat",
            "Tell everyone your most embarrassing moment",
            "Act like a robot for 2 minutes"
        ]

    @commands.command(name='meme')
    async def meme(self, ctx):
        """Get a random meme"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://meme-api.herokuapp.com/gimme') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title=data['title'],
                            color=discord.Color.random()
                        )
                        embed.set_image(url=data['url'])
                        embed.set_footer(text=f"👍 {data['ups']} | r/{data['subreddit']}")
                        
                        await ctx.send(embed=embed)
                    else:
                        raise Exception("API Error")
        except:
            # Fallback meme responses
            fallback_memes = [
                "🐱 *Shows you a picture of a cat wearing sunglasses*",
                "🐕 *Displays a meme of a dog saying 'This is fine' while everything burns*",
                "😂 *Presents the classic 'Distracted Boyfriend' meme*",
                "🤔 *Shows you a 'Galaxy Brain' expanding meme*",
                "😎 *Displays 'Chuck Norris doesn't need memes, memes need Chuck Norris'*"
            ]
            
            embed = discord.Embed(
                title="😄 Random Meme",
                description=random.choice(fallback_memes),
                color=discord.Color.orange()
            )
            embed.set_footer(text="Meme API unavailable - showing fallback meme")
            await ctx.send(embed=embed)

    @commands.command(name='joke')
    async def joke(self, ctx):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? It got mugged!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why do we tell actors to 'break a leg?' Because every play has a cast!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why don't some couples go to the gym? Because some relationships don't work out!",
            "What do you call a sleeping bull? A bulldozer!"
        ]
        
        joke = random.choice(jokes)
        
        embed = discord.Embed(
            title="😂 Dad Joke Time!",
            description=joke,
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("😂")

    @commands.command(name='coinflip', aliases=['flip'])
    async def coinflip(self, ctx):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        emoji = "🪙" if result == "Heads" else "🎯"
        
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"The coin landed on: **{result}** {emoji}",
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='dice', aliases=['roll'])
    async def dice(self, ctx, sides: int = 6):
        """Roll a dice with specified sides"""
        if sides < 2:
            await ctx.send("❌ Dice must have at least 2 sides!")
            return
        if sides > 100:
            await ctx.send("❌ That's too many sides! Maximum is 100.")
            return
            
        result = random.randint(1, sides)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolling a {sides}-sided dice...\n\n**Result: {result}**",
            color=discord.Color.red()
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='truthordare', aliases=['tod'])
    async def truth_or_dare(self, ctx, choice: str = None):
        """Play truth or dare"""
        if not choice or choice.lower() not in ['truth', 'dare']:
            embed = discord.Embed(
                title="😈 Truth or Dare",
                description="Choose: `!truthordare truth` or `!truthordare dare`",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            return
            
        if choice.lower() == 'truth':
            question = random.choice(self.truth_questions)
            embed = discord.Embed(
                title="🤔 Truth Question",
                description=question,
                color=discord.Color.blue()
            )
        else:
            dare = random.choice(self.dare_challenges)
            embed = discord.Embed(
                title="😈 Dare Challenge",
                description=dare,
                color=discord.Color.red()
            )
            
        await ctx.send(embed=embed)

    @commands.command(name='ship')
    async def ship(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        """Calculate compatibility between two users"""
        if not user1:
            user1 = ctx.author
        if not user2:
            await ctx.send("❌ Please mention another user to ship with!")
            return
            
        # Generate compatibility score
        compatibility = random.randint(1, 100)
        
        # Create ship name
        name1 = user1.display_name[:len(user1.display_name)//2]
        name2 = user2.display_name[len(user2.display_name)//2:]
        ship_name = name1 + name2
        
        # Determine compatibility level
        if compatibility >= 90:
            level = "💕 Perfect Match!"
            color = discord.Color.gold()
        elif compatibility >= 70:
            level = "❤️ Great Match!"
            color = discord.Color.red()
        elif compatibility >= 50:
            level = "💛 Good Match!"
            color = discord.Color.orange()
        elif compatibility >= 30:
            level = "💙 Could Work!"
            color = discord.Color.blue()
        else:
            level = "💔 Not Compatible"
            color = discord.Color.dark_red()
            
        embed = discord.Embed(
            title="💕 Love Calculator",
            description=f"**{user1.display_name}** + **{user2.display_name}** = **{ship_name}**",
            color=color
        )
        
        embed.add_field(name="Compatibility", value=f"**{compatibility}%**", inline=True)
        embed.add_field(name="Result", value=level, inline=True)
        
        # Create compatibility bar
        filled = int(compatibility / 10)
        empty = 10 - filled
        bar = "💖" * filled + "💔" * empty
        embed.add_field(name="Love Meter", value=bar, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='compliment')
    async def compliment(self, ctx, user: discord.Member = None):
        """Give someone a compliment"""
        if user is None:
            user = ctx.author
            
        compliments = [
            "You're an amazing person!",
            "Your smile brightens everyone's day!",
            "You have such a great sense of humor!",
            "You're incredibly talented!",
            "You make the world a better place!",
            "You're one of a kind!",
            "You have such a positive energy!",
            "You're absolutely wonderful!",
            "You inspire others just by being yourself!",
            "You're proof that good people exist!"
        ]
        
        compliment = random.choice(compliments)
        
        embed = discord.Embed(
            title="💝 Compliment",
            description=f"{user.mention}: {compliment}",
            color=discord.Color.pink()
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='quote')
    async def quote(self, ctx):
        """Get an inspirational quote"""
        quotes = [
            "\"The only way to do great work is to love what you do.\" - Steve Jobs",
            "\"Innovation distinguishes between a leader and a follower.\" - Steve Jobs",
            "\"Life is what happens to you while you're busy making other plans.\" - John Lennon",
            "\"The future belongs to those who believe in the beauty of their dreams.\" - Eleanor Roosevelt",
            "\"It is during our darkest moments that we must focus to see the light.\" - Aristotle",
            "\"The way to get started is to quit talking and begin doing.\" - Walt Disney",
            "\"Don't let yesterday take up too much of today.\" - Will Rogers",
            "\"You learn more from failure than from success.\" - Bram Stoker",
            "\"It's not whether you get knocked down, it's whether you get up.\" - Vince Lombardi",
            "\"If you are working on something exciting that you really care about, you don't have to be pushed.\" - Steve Jobs"
        ]
        
        quote = random.choice(quotes)
        
        embed = discord.Embed(
            title="✨ Inspirational Quote",
            description=quote,
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='hug')
    async def hug(self, ctx, user: discord.Member = None):
        """Give someone a hug"""
        if user is None:
            await ctx.send("❌ Who do you want to hug?")
            return
            
        if user == ctx.author:
            embed = discord.Embed(
                title="🤗 Self Hug",
                description=f"{ctx.author.mention} hugs themselves! Sometimes we all need self-love! 💕",
                color=discord.Color.pink()
            )
        else:
            embed = discord.Embed(
                title="🤗 Hug",
                description=f"{ctx.author.mention} gives {user.mention} a big warm hug! 🤗💕",
                color=discord.Color.pink()
            )
            
        await ctx.send(embed=embed)

    @commands.command(name='pat')
    async def pat(self, ctx, user: discord.Member = None):
        """Pat someone's head"""
        if user is None:
            await ctx.send("❌ Who do you want to pat?")
            return
            
        if user == ctx.author:
            embed = discord.Embed(
                title="👋 Self Pat",
                description=f"{ctx.author.mention} pats their own head! Good job! ✨",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="👋 Head Pat",
                description=f"{ctx.author.mention} gently pats {user.mention}'s head! *pat pat* 👋✨",
                color=discord.Color.green()
            )
            
        await ctx.send(embed=embed)

    @commands.command(name='kiss')
    async def kiss(self, ctx, user: discord.Member = None):
        """Give someone a kiss"""
        if user is None:
            await ctx.send("❌ Who do you want to kiss?")
            return
            
        if user == ctx.author:
            embed = discord.Embed(
                title="😘 Self Love",
                description=f"{ctx.author.mention} blows themselves a kiss! Self-love is important! 💋",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="😘 Kiss",
                description=f"{ctx.author.mention} gives {user.mention} a sweet kiss! 😘💕",
                color=discord.Color.red()
            )
            
        await ctx.send(embed=embed)

    @commands.command(name='confession')
    async def confession(self, ctx, *, message: str = None):
        """Make an anonymous confession"""
        if not message:
            await ctx.send("❌ Please provide a confession message!")
            return
            
        # Delete the original message for anonymity
        try:
            await ctx.message.delete()
        except:
            pass
            
        embed = discord.Embed(
            title="🤫 Anonymous Confession",
            description=message,
            color=discord.Color.dark_purple()
        )
        
        embed.set_footer(text="This confession was submitted anonymously")
        
        await ctx.send(embed=embed)

    @commands.command(name='marry')
    async def marry(self, ctx, user: discord.Member = None):
        """Propose marriage to someone"""
        if user is None:
            await ctx.send("❌ Who do you want to propose to?")
            return
            
        if user == ctx.author:
            await ctx.send("❌ You can't marry yourself! Though self-love is important! 💕")
            return
            
        if user.bot:
            await ctx.send("❌ You can't marry a bot! (Though I'm flattered 😊)")
            return
            
        embed = discord.Embed(
            title="💍 Marriage Proposal",
            description=f"{ctx.author.mention} has proposed to {user.mention}!\n\n💕 Will you marry them? 💕",
            color=discord.Color.pink()
        )
        
        embed.add_field(
            name="React to respond:",
            value="💍 = Yes, I do!\n💔 = Sorry, no...",
            inline=False
        )
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("💍")
        await message.add_reaction("💔")
        
        try:
            def check(reaction, reactor):
                return reactor == user and str(reaction.emoji) in ["💍", "💔"] and reaction.message.id == message.id
                
            reaction, reactor = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            
            if str(reaction.emoji) == "💍":
                # Marriage accepted
                user_data = self.bot.db.get_user(str(ctx.author.id))
                partner_data = self.bot.db.get_user(str(user.id))
                
                # Update marriage status
                self.bot.db.update_user_data(str(ctx.author.id), {'married_to': str(user.id)})
                self.bot.db.update_user_data(str(user.id), {'married_to': str(ctx.author.id)})
                
                embed = discord.Embed(
                    title="💕 Congratulations!",
                    description=f"{ctx.author.mention} and {user.mention} are now married! 🎉💍\n\nMay your love last forever! 💕",
                    color=discord.Color.gold()
                )
                
                # Give marriage bonus coins
                self.bot.db.add_coins(str(ctx.author.id), 500)
                self.bot.db.add_coins(str(user.id), 500)
                embed.add_field(name="💰 Wedding Gift", value="500 coins each!", inline=True)
                
            else:
                embed = discord.Embed(
                    title="💔 Proposal Declined",
                    description=f"{user.mention} said no to {ctx.author.mention}'s proposal.\n\nDon't worry, there are plenty of fish in the sea! 🐟",
                    color=discord.Color.red()
                )
                
            await message.edit(embed=embed)
            
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="⏰ Proposal Expired",
                description="The proposal timed out. Maybe try again later?",
                color=discord.Color.orange()
            )
            await message.edit(embed=embed)

    @commands.command(name='divorce')
    async def divorce(self, ctx):
        """End your marriage"""
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        if 'married_to' not in user_data or not user_data['married_to']:
            await ctx.send("❌ You're not married!")
            return
            
        partner_id = user_data['married_to']
        
        try:
            partner = await self.bot.fetch_user(int(partner_id))
            
            embed = discord.Embed(
                title="💔 Divorce",
                description=f"{ctx.author.mention} and {partner.mention} have divorced.\n\nSometimes things just don't work out. 💔",
                color=discord.Color.red()
            )
            
            # Remove marriage status
            self.bot.db.update_user_data(user_id, {'married_to': None})
            self.bot.db.update_user_data(partner_id, {'married_to': None})
            
            await ctx.send(embed=embed)
            
        except:
            # Partner not found, just remove marriage status
            self.bot.db.update_user_data(user_id, {'married_to': None})
            await ctx.send("💔 Your marriage has been ended.")

    @commands.command(name='profile')
    async def profile(self, ctx, user: discord.Member = None):
        """View someone's extended profile"""
        if user is None:
            user = ctx.author
            
        user_data = self.bot.db.get_user(str(user.id))
        
        embed = discord.Embed(
            title=f"👤 {user.display_name}'s Profile",
            color=user.color if user.color != discord.Color.default() else discord.Color.blue()
        )
        
        embed.set_thumbnail(url=user.display_avatar.url)
        
        # Basic info
        embed.add_field(name="💰 Coins", value=f"{user_data['coins']:,}", inline=True)
        embed.add_field(name="📊 Commands Used", value=user_data.get('total_commands', 0), inline=True)
        
        # Marriage status
        if user_data.get('married_to'):
            try:
                partner = await self.bot.fetch_user(int(user_data['married_to']))
                embed.add_field(name="💕 Married to", value=partner.display_name, inline=True)
            except:
                embed.add_field(name="💕 Status", value="Single", inline=True)
        else:
            embed.add_field(name="💕 Status", value="Single", inline=True)
            
        # Game stats
        embed.add_field(name="🎮 Trivia Wins", value=user_data.get('trivia_wins', 0), inline=True)
        embed.add_field(name="💼 Work Sessions", value=user_data.get('total_work_sessions', 0), inline=True)
        embed.add_field(name="🔥 Work Streak", value=user_data.get('work_streak', 0), inline=True)
        
        # Account creation
        embed.add_field(
            name="📅 Joined Discord",
            value=user.created_at.strftime("%B %d, %Y"),
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FunCog(bot))
