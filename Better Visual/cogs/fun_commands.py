
import discord
from discord.ext import commands
import random
import asyncio
import json
from datetime import datetime

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

    @commands.command(name='truth')
    async def truth(self, ctx):
        """Get a random truth question"""
        question = random.choice(self.truth_questions)
        
        embed = discord.Embed(
            title="🤔 Truth Question",
            description=question,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Question for {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name='dare')
    async def dare(self, ctx):
        """Get a random dare challenge"""
        challenge = random.choice(self.dare_challenges)
        
        embed = discord.Embed(
            title="😈 Dare Challenge",
            description=challenge,
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Dare for {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name='roast')
    async def roast(self, ctx, member: discord.Member = None):
        """Roast someone (friendly fun)"""
        target = member or ctx.author
        
        roasts = [
            f"{target.mention}, you're like a software update. Whenever I see you, I think 'not now'.",
            f"{target.mention}, if you were a vegetable, you'd be a cute-cumber... wait, that's a compliment. Never mind!",
            f"{target.mention}, you're not stupid; you just have bad luck thinking.",
            f"{target.mention}, I'd roast you, but my mom said I'm not allowed to burn trash.",
            f"{target.mention}, you're like a penny - two-faced and not worth much!",
            f"{target.mention}, if laughter is the best medicine, your face must be curing the world!",
            f"{target.mention}, you're so bright, you make the sun look dim... in an eclipse!",
            f"{target.mention}, you're like WiFi - I can't see you but I know you're not working properly."
        ]
        
        roast = random.choice(roasts)
        
        embed = discord.Embed(
            title="🔥 Roast Time!",
            description=roast,
            color=discord.Color.orange()
        )
        embed.set_footer(text="This is all in good fun! 😄")
        await ctx.send(embed=embed)

    @commands.command(name='fact')
    async def random_fact(self, ctx):
        """Get a random fun fact"""
        facts = [
            "Honey never spoils. Archaeologists have found 3000-year-old honey that's still perfectly edible!",
            "A group of flamingos is called a 'flamboyance'.",
            "Bananas are berries, but strawberries aren't!",
            "Octopuses have three hearts and blue blood.",
            "A shrimp's heart is in its head.",
            "It's impossible to hum while holding your nose.",
            "Dolphins have names for each other.",
            "A group of pandas is called an 'embarrassment'.",
            "The shortest war in history lasted only 38-45 minutes.",
            "Bubble wrap was originally invented as wallpaper."
        ]
        
        fact = random.choice(facts)
        
        embed = discord.Embed(
            title="🧠 Random Fact",
            description=fact,
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='wouldyourather', aliases=['wyr'])
    async def would_you_rather(self, ctx):
        """Get a would you rather question"""
        questions = [
            "Would you rather have the ability to fly or be invisible?",
            "Would you rather always be 10 minutes late or 20 minutes early?",
            "Would you rather have unlimited money or unlimited time?",
            "Would you rather never use social media again or never watch another movie?",
            "Would you rather be able to speak all languages or talk to animals?",
            "Would you rather live without music or without television?",
            "Would you rather have super strength or super speed?",
            "Would you rather never have to sleep or never have to eat?",
            "Would you rather be famous or have a happy family life?",
            "Would you rather live in the past or the future?"
        ]
        
        question = random.choice(questions)
        
        embed = discord.Embed(
            title="🤷 Would You Rather",
            description=question,
            color=discord.Color.purple()
        )
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")

    @commands.command(name='rate')
    async def rate(self, ctx, *, thing=None):
        """Rate something on a scale of 1-10"""
        if not thing:
            await ctx.send("❌ What do you want me to rate?\nExample: `!rate pizza`")
            return
            
        rating = random.randint(1, 10)
        
        if rating <= 3:
            reaction = "😢 Not great..."
        elif rating <= 5:
            reaction = "😐 It's okay"
        elif rating <= 7:
            reaction = "😊 Pretty good!"
        elif rating <= 9:
            reaction = "😍 Amazing!"
        else:
            reaction = "🤩 PERFECT!"
        
        embed = discord.Embed(
            title="⭐ Rating",
            description=f"I rate **{thing}** a **{rating}/10**!\n{reaction}",
            color=discord.Color.gold()
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='choose')
    async def choose(self, ctx, *, choices=None):
        """Choose between multiple options"""
        if not choices:
            await ctx.send("❌ Give me some choices!\nExample: `!choose pizza, burger, tacos`")
            return
            
        # Split choices by comma or 'or'
        if ',' in choices:
            options = [choice.strip() for choice in choices.split(',')]
        elif ' or ' in choices.lower():
            options = [choice.strip() for choice in choices.lower().split(' or ')]
        else:
            await ctx.send("❌ Please separate choices with commas or 'or'\nExample: `!choose pizza, burger, tacos`")
            return
        
        if len(options) < 2:
            await ctx.send("❌ I need at least 2 choices to pick from!")
            return
            
        choice = random.choice(options)
        
        embed = discord.Embed(
            title="🎯 My Choice",
            description=f"I choose: **{choice}**",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="All Options",
            value=", ".join(options),
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='joke')
    async def joke(self, ctx):
        """Tell a random joke"""
        jokes = [
            ("Why don't scientists trust atoms?", "Because they make up everything!"),
            ("Why did the scarecrow win an award?", "He was outstanding in his field!"),
            ("Why don't eggs tell jokes?", "They'd crack each other up!"),
            ("What do you call a fake noodle?", "An impasta!"),
            ("Why did the math book look so sad?", "Because it had too many problems!"),
            ("What do you call a bear with no teeth?", "A gummy bear!"),
            ("Why can't a bicycle stand up by itself?", "Because it's two tired!"),
            ("What do you call a fish wearing a crown?", "A king fish!"),
            ("Why don't skeletons fight each other?", "They don't have the guts!"),
            ("What's orange and sounds like a parrot?", "A carrot!")
        ]
        
        setup, punchline = random.choice(jokes)
        
        embed = discord.Embed(
            title="😂 Joke Time",
            description=setup,
            color=discord.Color.yellow()
        )
        
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        
        embed.add_field(name="Punchline", value=punchline, inline=False)
        await message.edit(embed=embed)
        await message.add_reaction("😂")

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

async def setup(bot):
    await bot.add_cog(FunCog(bot))
