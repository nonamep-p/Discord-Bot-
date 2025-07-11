
import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime

class SocialCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.confession_channel = None
        self.confession_count = 0

    @commands.command(name='hug')
    async def hug(self, ctx, member: discord.Member = None):
        """Hug someone!"""
        if not member:
            await ctx.send("Who do you want to hug? Mention someone! 🤗")
            return
            
        if member == ctx.author:
            await ctx.send(f"*{ctx.author.display_name} hugs themselves* 🤗 Self-love is important!")
            return
            
        hug_gifs = [
            "https://tenor.com/view/hug-anime-cute-gif-12153390",
            "https://tenor.com/view/hug-anime-wholesome-gif-13032845",
            "https://tenor.com/view/virtual-hug-gif-25177331"
        ]
        
        embed = discord.Embed(
            title="🤗 Hug!",
            description=f"{ctx.author.display_name} hugs {member.display_name}!",
            color=discord.Color.pink()
        )
        embed.set_image(url=random.choice(hug_gifs))
        await ctx.send(embed=embed)

    @commands.command(name='pat')
    async def pat(self, ctx, member: discord.Member = None):
        """Pat someone's head!"""
        if not member:
            await ctx.send("Who do you want to pat? Mention someone! 🫳")
            return
            
        if member == ctx.author:
            await ctx.send(f"*{ctx.author.display_name} pats their own head* 🫳 Good job!")
            return
            
        embed = discord.Embed(
            title="🫳 Head Pat!",
            description=f"{ctx.author.display_name} pats {member.display_name}'s head!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name='ship')
    async def ship(self, ctx, member1: discord.Member = None, member2: discord.Member = None):
        """Ship two people together!"""
        if not member1:
            member1 = ctx.author
        if not member2:
            await ctx.send("Mention someone to ship with! 💕")
            return
            
        # Calculate ship percentage (deterministic based on user IDs)
        combined_id = str(member1.id) + str(member2.id)
        ship_score = (hash(combined_id) % 101)
        
        # Create ship name
        name1 = member1.display_name[:len(member1.display_name)//2]
        name2 = member2.display_name[len(member2.display_name)//2:]
        ship_name = name1 + name2
        
        # Determine reaction based on score
        if ship_score >= 80:
            reaction = "💖 Perfect match!"
            color = discord.Color.red()
        elif ship_score >= 60:
            reaction = "💕 Great compatibility!"
            color = discord.Color.pink()
        elif ship_score >= 40:
            reaction = "💛 Good friends!"
            color = discord.Color.yellow()
        elif ship_score >= 20:
            reaction = "🤝 Could work!"
            color = discord.Color.blue()
        else:
            reaction = "💔 Better as friends!"
            color = discord.Color.light_grey()
        
        embed = discord.Embed(
            title="💕 Ship Calculator",
            description=f"**{member1.display_name}** + **{member2.display_name}** = **{ship_name}**",
            color=color
        )
        embed.add_field(name="Compatibility", value=f"**{ship_score}%**", inline=True)
        embed.add_field(name="Result", value=reaction, inline=True)
        
        # Create progress bar
        filled = "💖" * (ship_score // 10)
        empty = "🤍" * (10 - ship_score // 10)
        progress_bar = filled + empty
        embed.add_field(name="Love Meter", value=progress_bar, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='compliment')
    async def compliment(self, ctx, member: discord.Member = None):
        """Give someone a compliment!"""
        target = member or ctx.author
        
        compliments = [
            "You're absolutely amazing! ✨",
            "Your creativity knows no bounds! 🎨",
            "You light up every room you enter! 💡",
            "You're incredibly thoughtful and kind! 💕",
            "Your sense of humor is fantastic! 😄",
            "You're so talented and skilled! 🌟",
            "You have such a positive energy! ⚡",
            "You're an inspiration to others! 🚀",
            "Your intelligence is impressive! 🧠",
            "You're genuinely awesome! 🔥"
        ]
        
        compliment = random.choice(compliments)
        
        embed = discord.Embed(
            title="✨ Compliment",
            description=f"{target.mention} {compliment}",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Compliment from {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @commands.command(name='confession')
    async def confession(self, ctx, *, message: str = None):
        """Submit an anonymous confession"""
        if not message:
            await ctx.send("Write your confession! Example: `!confession I love pizza more than people` 🤫")
            return
            
        if len(message) > 500:
            await ctx.send("Confession too long! Keep it under 500 characters 📝")
            return
            
        self.confession_count += 1
        
        embed = discord.Embed(
            title="🤫 Anonymous Confession",
            description=message,
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Confession #{self.confession_count}")
        
        await ctx.send(embed=embed)
        
        # Delete the original message for anonymity
        try:
            await ctx.message.delete()
        except:
            pass

    @commands.command(name='quote')
    async def inspirational_quote(self, ctx):
        """Get an inspirational quote"""
        quotes = [
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
            ("Life is what happens to you while you're busy making other plans.", "John Lennon"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
            ("The only impossible journey is the one you never begin.", "Tony Robbins"),
            ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
            ("The way to get started is to quit talking and begin doing.", "Walt Disney")
        ]
        
        quote, author = random.choice(quotes)
        
        embed = discord.Embed(
            title="💭 Inspirational Quote",
            description=f"*\"{quote}\"*",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"— {author}")
        await ctx.send(embed=embed)

    @commands.command(name='marry')
    async def marry(self, ctx, member: discord.Member = None):
        """Propose marriage to someone!"""
        if not member:
            await ctx.send("Who do you want to marry? Mention someone! 💍")
            return
            
        if member == ctx.author:
            await ctx.send("You can't marry yourself! Though self-love is important 💕")
            return
            
        if member.bot:
            await ctx.send("You can't marry a bot! We're just friends 🤖")
            return
        
        embed = discord.Embed(
            title="💍 Marriage Proposal!",
            description=f"{ctx.author.mention} proposes to {member.mention}!",
            color=discord.Color.pink()
        )
        embed.add_field(
            name="💕 Will you marry them?",
            value="React with 💍 to accept or 💔 to decline!",
            inline=False
        )
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("💍")
        await message.add_reaction("💔")
        
        def check(reaction, user):
            return user == member and str(reaction.emoji) in ["💍", "💔"] and reaction.message.id == message.id
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            
            if str(reaction.emoji) == "💍":
                result_embed = discord.Embed(
                    title="🎉 Marriage Accepted!",
                    description=f"Congratulations! {ctx.author.mention} and {member.mention} are now married! 💕",
                    color=discord.Color.green()
                )
            else:
                result_embed = discord.Embed(
                    title="💔 Marriage Declined",
                    description=f"{member.mention} declined the proposal. Better luck next time!",
                    color=discord.Color.red()
                )
                
            await message.edit(embed=result_embed)
            
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title="⏰ Proposal Expired",
                description="The proposal timed out. No response received!",
                color=discord.Color.grey()
            )
            await message.edit(embed=timeout_embed)

async def setup(bot):
    await bot.add_cog(SocialCog(bot))
