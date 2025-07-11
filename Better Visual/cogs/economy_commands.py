
import discord
from discord.ext import commands
import random
import time
import json
from datetime import datetime, timedelta

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_cooldowns = {}
        self.work_cooldowns = {}

    def get_user_coins(self, user_id):
        """Get user's coin balance"""
        user_data = self.bot.db.get_user(str(user_id))
        return user_data.get('coins', 0) if user_data else 0
    
    def add_coins(self, user_id, amount):
        """Add coins to user"""
        current = self.get_user_coins(user_id)
        self.bot.db.update_user(str(user_id), {'coins': current + amount})
        return current + amount

    @commands.command(name='balance', aliases=['bal', 'coins'])
    async def balance(self, ctx, member: discord.Member = None):
        """Check coin balance"""
        target = member or ctx.author
        coins = self.get_user_coins(target.id)
        
        embed = discord.Embed(
            title="💰 Coin Balance",
            description=f"{target.display_name} has **{coins:,}** coins!",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=target.avatar.url if target.avatar else None)
        await ctx.send(embed=embed)

    @commands.command(name='daily')
    async def daily_reward(self, ctx):
        """Claim daily coins"""
        user_id = str(ctx.author.id)
        now = time.time()
        
        if user_id in self.daily_cooldowns:
            time_left = self.daily_cooldowns[user_id] - now
            if time_left > 0:
                hours = int(time_left // 3600)
                minutes = int((time_left % 3600) // 60)
                await ctx.send(f"⏰ Daily reward already claimed! Come back in {hours}h {minutes}m")
                return
        
        # Set 24-hour cooldown
        self.daily_cooldowns[user_id] = now + 86400
        
        # Random daily reward
        base_reward = random.randint(100, 500)
        streak_bonus = random.randint(0, 200)
        total_reward = base_reward + streak_bonus
        
        new_balance = self.add_coins(ctx.author.id, total_reward)
        
        embed = discord.Embed(
            title="🎁 Daily Reward Claimed!",
            description=f"You received **{total_reward:,}** coins!",
            color=discord.Color.green()
        )
        embed.add_field(name="Base Reward", value=f"{base_reward:,} coins", inline=True)
        embed.add_field(name="Streak Bonus", value=f"{streak_bonus:,} coins", inline=True)
        embed.add_field(name="New Balance", value=f"{new_balance:,} coins", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='work')
    async def work(self, ctx):
        """Work for coins"""
        user_id = str(ctx.author.id)
        now = time.time()
        
        if user_id in self.work_cooldowns:
            time_left = self.work_cooldowns[user_id] - now
            if time_left > 0:
                minutes = int(time_left // 60)
                seconds = int(time_left % 60)
                await ctx.send(f"⏰ You're tired! Rest for {minutes}m {seconds}s before working again")
                return
        
        # Set 1-hour cooldown
        self.work_cooldowns[user_id] = now + 3600
        
        jobs = [
            ("programming", "💻", random.randint(50, 150)),
            ("cooking", "👨‍🍳", random.randint(30, 120)),
            ("gardening", "🌱", random.randint(40, 100)),
            ("teaching", "📚", random.randint(60, 140)),
            ("streaming", "📹", random.randint(20, 200)),
            ("art", "🎨", random.randint(70, 180))
        ]
        
        job_name, emoji, reward = random.choice(jobs)
        new_balance = self.add_coins(ctx.author.id, reward)
        
        embed = discord.Embed(
            title=f"{emoji} Work Complete!",
            description=f"You worked as a {job_name} and earned **{reward:,}** coins!",
            color=discord.Color.blue()
        )
        embed.add_field(name="New Balance", value=f"{new_balance:,} coins", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='gamble', aliases=['bet'])
    async def gamble(self, ctx, amount: int = None):
        """Gamble your coins"""
        if not amount:
            await ctx.send("Specify an amount to gamble! Example: `!gamble 100` 🎰")
            return
            
        if amount < 10:
            await ctx.send("Minimum bet is 10 coins! 💰")
            return
            
        current_coins = self.get_user_coins(ctx.author.id)
        if amount > current_coins:
            await ctx.send(f"You don't have enough coins! You have {current_coins:,} coins 💸")
            return
        
        # 45% chance to win
        if random.random() < 0.45:
            # Win between 1.5x to 3x
            multiplier = random.uniform(1.5, 3.0)
            winnings = int(amount * multiplier)
            new_balance = self.add_coins(ctx.author.id, winnings - amount)
            
            embed = discord.Embed(
                title="🎉 You Won!",
                description=f"You won **{winnings:,}** coins! (x{multiplier:.1f})",
                color=discord.Color.green()
            )
            embed.add_field(name="New Balance", value=f"{new_balance:,} coins", inline=False)
        else:
            # Lose
            new_balance = self.add_coins(ctx.author.id, -amount)
            
            embed = discord.Embed(
                title="💸 You Lost!",
                description=f"You lost **{amount:,}** coins!",
                color=discord.Color.red()
            )
            embed.add_field(name="New Balance", value=f"{new_balance:,} coins", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='shop')
    async def shop(self, ctx):
        """View the coin shop"""
        embed = discord.Embed(
            title="🛍️ Coin Shop",
            description="Spend your coins on cool items!",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="🎭 Custom Role Color",
            value="**2,000 coins** - Get a custom colored role!",
            inline=False
        )
        embed.add_field(
            name="⭐ VIP Status",
            value="**5,000 coins** - Get VIP perks for 30 days!",
            inline=False
        )
        embed.add_field(
            name="🎪 Custom Nickname",
            value="**1,000 coins** - Set a custom nickname!",
            inline=False
        )
        
        embed.set_footer(text="Use !buy <item> to purchase! More items coming soon!")
        await ctx.send(embed=embed)

    @commands.command(name='leaderboard', aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        """Show coin leaderboard"""
        # This would need database implementation to work fully
        embed = discord.Embed(
            title="🏆 Coin Leaderboard",
            description="Top 10 richest users:",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="Coming Soon!",
            value="Leaderboard will show the richest users 💰",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
