
import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
import json
from datetime import datetime

class EntertainmentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}
        self.confession_count = 0

    @commands.command(name='poll')
    async def create_poll(self, ctx, question: str = None, *options):
        """Create a poll with multiple options"""
        if not question:
            await ctx.send("❌ Please provide a question!\nExample: `!poll \"What's your favorite color?\" Red Blue Green`")
            return
            
        if len(options) < 2:
            await ctx.send("❌ Please provide at least 2 options!")
            return
            
        if len(options) > 10:
            await ctx.send("❌ Maximum 10 options allowed!")
            return
            
        embed = discord.Embed(
            title="📊 Poll",
            description=question,
            color=discord.Color.blue()
        )
        
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        poll_text = ""
        for i, option in enumerate(options):
            poll_text += f"{reactions[i]} {option}\n"
            
        embed.add_field(name="Options", value=poll_text, inline=False)
        embed.set_footer(text=f"Poll by {ctx.author.display_name}")
        
        message = await ctx.send(embed=embed)
        
        for i in range(len(options)):
            await message.add_reaction(reactions[i])

    @commands.command(name='riddle')
    async def riddle(self, ctx):
        """Get a random riddle to solve"""
        riddles = [
            ("What has keys but no locks, space but no room, and you can enter but can't go inside?", "a keyboard"),
            ("What gets wet while drying?", "a towel"),
            ("What has a thumb and four fingers but isn't alive?", "a glove"),
            ("What goes up but never comes down?", "your age"),
            ("What has cities but no houses, forests but no trees, and water but no fish?", "a map"),
            ("I'm tall when I'm young and short when I'm old. What am I?", "a candle"),
            ("What breaks but never falls, and what falls but never breaks?", "day breaks and night falls"),
            ("What gets bigger the more you take away from it?", "a hole")
        ]
        
        riddle_text, answer = random.choice(riddles)
        
        embed = discord.Embed(
            title="🧩 Riddle Time!",
            description=riddle_text,
            color=discord.Color.purple()
        )
        embed.set_footer(text="Think you know the answer? 🤔")
        
        await ctx.send(embed=embed)
        
        # Store the answer for checking
        self.bot.pending_riddles = getattr(self.bot, 'pending_riddles', {})
        self.bot.pending_riddles[ctx.channel.id] = answer.lower()
        
        # Auto-reveal after 60 seconds
        await asyncio.sleep(60)
        if ctx.channel.id in self.bot.pending_riddles:
            reveal_embed = discord.Embed(
                title="🧩 Riddle Answer",
                description=f"The answer was: **{answer}**",
                color=discord.Color.gold()
            )
            await ctx.send(embed=reveal_embed)
            del self.bot.pending_riddles[ctx.channel.id]

    @commands.command(name='fortune')
    async def fortune_cookie(self, ctx):
        """Get your fortune cookie message"""
        fortunes = [
            "Your future is bright and full of possibilities! ✨",
            "A pleasant surprise awaits you soon! 🎁",
            "Success comes to those who dare to begin! 🚀",
            "Your hard work will soon pay off! 💪",
            "Today is a good day to make new friends! 👥",
            "Adventure is on the horizon! 🌅",
            "Trust your instincts - they're right! 🎯",
            "Something wonderful is about to happen! 🌟",
            "Your creativity will lead to great things! 🎨",
            "Kindness will come back to you tenfold! 💕"
        ]
        
        fortune = random.choice(fortunes)
        
        embed = discord.Embed(
            title="🥠 Fortune Cookie",
            description=fortune,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Fortune for {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name='moodmeter')
    async def mood_meter(self, ctx, member: discord.Member = None):
        """Check someone's mood level"""
        target = member or ctx.author
        
        mood_level = random.randint(1, 100)
        
        if mood_level >= 80:
            mood_desc = "😄 Extremely Happy!"
            color = discord.Color.green()
        elif mood_level >= 60:
            mood_desc = "😊 Pretty Good!"
            color = discord.Color.blue()
        elif mood_level >= 40:
            mood_desc = "😐 Neutral"
            color = discord.Color.yellow()
        elif mood_level >= 20:
            mood_desc = "😕 Bit Down"
            color = discord.Color.orange()
        else:
            mood_desc = "😢 Needs Cheering Up"
            color = discord.Color.red()
            
        embed = discord.Embed(
            title="🌡️ Mood Meter",
            description=f"{target.display_name}'s mood: **{mood_level}%**\n{mood_desc}",
            color=color
        )
        
        # Create mood bar
        filled = "🟢" * (mood_level // 10)
        empty = "⚪" * (10 - mood_level // 10)
        mood_bar = filled + empty
        embed.add_field(name="Mood Level", value=mood_bar, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='advice')
    async def life_advice(self, ctx):
        """Get some life advice"""
        advice_list = [
            "Be yourself; everyone else is already taken. 💭",
            "The only way to do great work is to love what you do. 💪",
            "Life is what happens when you're busy making other plans. 🌟",
            "Don't let yesterday take up too much of today. ⏰",
            "You learn more from failure than from success. 📚",
            "It's never too late to be what you might have been. 🚀",
            "The best time to plant a tree was 20 years ago. The second best time is now. 🌱",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. 🎯"
        ]
        
        advice = random.choice(advice_list)
        
        embed = discord.Embed(
            title="💡 Life Advice",
            description=advice,
            color=discord.Color.teal()
        )
        embed.set_footer(text="Take it with a grain of salt! 🧂")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Check riddle answers"""
        if message.author.bot:
            return
            
        pending_riddles = getattr(self.bot, 'pending_riddles', {})
        if message.channel.id in pending_riddles:
            answer = pending_riddles[message.channel.id]
            if answer in message.content.lower():
                embed = discord.Embed(
                    title="🎉 Correct Answer!",
                    description=f"Well done {message.author.mention}! The answer was indeed **{answer}**!",
                    color=discord.Color.green()
                )
                await message.channel.send(embed=embed)
                del pending_riddles[message.channel.id]

async def setup(bot):
    await bot.add_cog(EntertainmentCog(bot))
