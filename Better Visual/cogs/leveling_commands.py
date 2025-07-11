
import discord
from discord.ext import commands
import random
import math
import time
from datetime import datetime

class LevelingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_cooldowns = {}
        self.level_roles = {}  # guild_id -> {level: role_id}
        
    def calculate_level(self, xp):
        """Calculate level from XP"""
        return int(math.sqrt(xp / 100))
    
    def calculate_xp_for_level(self, level):
        """Calculate XP needed for a specific level"""
        return level * level * 100
    
    def get_user_data(self, user_id):
        """Get user XP and level data"""
        user_data = self.bot.db.get_user(str(user_id))
        xp = user_data.get('xp', 0) if user_data else 0
        level = self.calculate_level(xp)
        return xp, level

    @commands.Cog.listener()
    async def on_message(self, message):
        """Give XP for messages"""
        if message.author.bot:
            return
            
        user_id = str(message.author.id)
        current_time = time.time()
        
        # XP cooldown (60 seconds)
        if user_id in self.xp_cooldowns:
            if current_time - self.xp_cooldowns[user_id] < 60:
                return
        
        self.xp_cooldowns[user_id] = current_time
        
        # Get current XP and level
        old_xp, old_level = self.get_user_data(message.author.id)
        
        # Add random XP (15-25 per message)
        xp_gain = random.randint(15, 25)
        new_xp = old_xp + xp_gain
        new_level = self.calculate_level(new_xp)
        
        # Update database
        user_data = self.bot.db.get_user(user_id) or {}
        user_data['xp'] = new_xp
        self.bot.db.update_user(user_id, user_data)
        
        # Check for level up
        if new_level > old_level:
            await self.handle_level_up(message, new_level)

    async def handle_level_up(self, message, new_level):
        """Handle level up rewards and announcements"""
        embed = discord.Embed(
            title="🎉 Level Up!",
            description=f"Congratulations {message.author.mention}! You've reached **Level {new_level}**!",
            color=discord.Color.gold()
        )
        
        # Calculate XP for next level
        next_level_xp = self.calculate_xp_for_level(new_level + 1)
        current_level_xp = self.calculate_xp_for_level(new_level)
        current_xp, _ = self.get_user_data(message.author.id)
        progress = current_xp - current_level_xp
        needed = next_level_xp - current_level_xp
        
        embed.add_field(
            name="Progress to Next Level",
            value=f"{progress}/{needed} XP",
            inline=True
        )
        
        # Level rewards
        rewards = []
        
        # Coin rewards
        coin_reward = new_level * 50
        user_data = self.bot.db.get_user(str(message.author.id))
        if user_data:
            current_coins = user_data.get('coins', 0)
            user_data['coins'] = current_coins + coin_reward
            self.bot.db.update_user(str(message.author.id), user_data)
            rewards.append(f"💰 {coin_reward} coins")
        
        # Special level rewards
        if new_level == 5:
            rewards.append("🎁 Welcome package unlocked!")
        elif new_level == 10:
            rewards.append("⭐ VIP status for 1 day!")
        elif new_level == 25:
            rewards.append("🎨 Custom role color unlocked!")
        elif new_level == 50:
            rewards.append("👑 Special title unlocked!")
        elif new_level % 20 == 0:  # Every 20 levels
            rewards.append("🎊 Milestone bonus: 1000 coins!")
            if user_data:
                user_data['coins'] = user_data.get('coins', 0) + 1000
                self.bot.db.update_user(str(message.author.id), user_data)
        
        if rewards:
            embed.add_field(
                name="🎁 Rewards",
                value="\n".join(rewards),
                inline=False
            )
        
        # Check for level roles
        if message.guild and message.guild.id in self.level_roles:
            guild_level_roles = self.level_roles[message.guild.id]
            if new_level in guild_level_roles:
                role = message.guild.get_role(guild_level_roles[new_level])
                if role:
                    try:
                        await message.author.add_roles(role)
                        embed.add_field(
                            name="🎭 Role Reward",
                            value=f"You've been given the {role.mention} role!",
                            inline=False
                        )
                    except:
                        pass
        
        await message.reply(embed=embed)

    @commands.command(name='rank', aliases=['level', 'xp'])
    async def rank(self, ctx, member: discord.Member = None):
        """Check rank/XP of a user"""
        target = member or ctx.author
        
        xp, level = self.get_user_data(target.id)
        
        if xp == 0:
            await ctx.send(f"📊 {target.display_name} hasn't gained any XP yet!")
            return
        
        # Calculate progress to next level
        current_level_xp = self.calculate_xp_for_level(level)
        next_level_xp = self.calculate_xp_for_level(level + 1)
        progress = xp - current_level_xp
        needed = next_level_xp - current_level_xp
        
        # Create progress bar
        progress_percentage = progress / needed
        bar_length = 20
        filled_length = int(bar_length * progress_percentage)
        bar = "█" * filled_length + "▒" * (bar_length - filled_length)
        
        embed = discord.Embed(
            title=f"📊 {target.display_name}'s Rank",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Level", value=f"**{level}**", inline=True)
        embed.add_field(name="Total XP", value=f"**{xp:,}**", inline=True)
        embed.add_field(name="Next Level", value=f"**{level + 1}**", inline=True)
        
        embed.add_field(
            name="Progress to Next Level",
            value=f"`{bar}` {progress}/{needed} XP",
            inline=False
        )
        
        if target.avatar:
            embed.set_thumbnail(url=target.avatar.url)
        
        await ctx.send(embed=embed)

    @commands.command(name='leaderboard', aliases=['lb'])
    async def leaderboard(self, ctx):
        """Show XP leaderboard for the server"""
        # This would need a proper database query to work efficiently
        embed = discord.Embed(
            title="🏆 XP Leaderboard",
            description="Top members by XP in this server:",
            color=discord.Color.gold()
        )
        
        # For now, show a placeholder
        embed.add_field(
            name="🥇 #1 - Example User",
            value="Level 25 • 62,500 XP",
            inline=False
        )
        embed.add_field(
            name="🥈 #2 - Another User", 
            value="Level 20 • 40,000 XP",
            inline=False
        )
        embed.add_field(
            name="🥉 #3 - Third User",
            value="Level 18 • 32,400 XP",
            inline=False
        )
        
        embed.set_footer(text="Leaderboard updates in real-time!")
        await ctx.send(embed=embed)

    @commands.command(name='setlevelrole')
    @commands.has_permissions(manage_roles=True)
    async def set_level_role(self, ctx, level: int, role: discord.Role):
        """Set a role reward for reaching a specific level"""
        if ctx.guild.id not in self.level_roles:
            self.level_roles[ctx.guild.id] = {}
        
        self.level_roles[ctx.guild.id][level] = role.id
        
        embed = discord.Embed(
            title="✅ Level Role Set",
            description=f"Users will receive {role.mention} when they reach **Level {level}**!",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='givexp')
    @commands.has_permissions(administrator=True)
    async def give_xp(self, ctx, member: discord.Member, amount: int):
        """Give XP to a user (Admin only)"""
        if amount < 1:
            await ctx.send("❌ XP amount must be positive!")
            return
        
        user_id = str(member.id)
        old_xp, old_level = self.get_user_data(member.id)
        new_xp = old_xp + amount
        new_level = self.calculate_level(new_xp)
        
        # Update database
        user_data = self.bot.db.get_user(user_id) or {}
        user_data['xp'] = new_xp
        self.bot.db.update_user(user_id, user_data)
        
        embed = discord.Embed(
            title="✅ XP Given",
            description=f"Gave **{amount:,} XP** to {member.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="New Total", value=f"{new_xp:,} XP", inline=True)
        embed.add_field(name="New Level", value=f"Level {new_level}", inline=True)
        
        await ctx.send(embed=embed)
        
        # Check for level up
        if new_level > old_level:
            level_embed = discord.Embed(
                title="🎉 Level Up!",
                description=f"{member.mention} jumped to **Level {new_level}**!",
                color=discord.Color.gold()
            )
            await ctx.send(embed=level_embed)

async def setup(bot):
    await bot.add_cog(LevelingCog(bot))
