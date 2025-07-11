
import discord
from discord.ext import commands
import random
import asyncio
import json
from datetime import datetime, timedelta, timezone
import logging
import sqlite3

logger = logging.getLogger(__name__)

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slot_emojis = ['🍎', '🍊', '🍋', '🍇', '🍒', '🍌', '💎', '⭐', '🔔', '💰']
        self.work_jobs = [
            {"name": "Pizza Delivery", "min": 50, "max": 150, "emoji": "🍕"},
            {"name": "Dog Walker", "min": 30, "max": 100, "emoji": "🐕"},
            {"name": "Programmer", "min": 100, "max": 300, "emoji": "💻"},
            {"name": "Uber Driver", "min": 75, "max": 200, "emoji": "🚗"},
            {"name": "Freelancer", "min": 80, "max": 250, "emoji": "💼"},
            {"name": "Streamer", "min": 20, "max": 500, "emoji": "📹"},
            {"name": "Chef", "min": 90, "max": 220, "emoji": "👨‍🍳"},
            {"name": "Artist", "min": 60, "max": 300, "emoji": "🎨"}
        ]
        
    @commands.command(name='work')
    async def work(self, ctx):
        """Work for coins (1 hour cooldown with exploit protection)"""
        user_id = str(ctx.author.id)
        
        # Check if user is banned
        user_data = self.bot.db.get_user(user_id)
        if user_data.get('is_banned', 0):
            await ctx.send("❌ You are banned from using economy commands.")
            return
        
        # Atomic cooldown check with database
        can_work, reason, time_left = self.bot.db.check_command_cooldown(user_id, 'work', 3600)  # 1 hour
        
        if not can_work:
            if time_left > 0:
                hours = int(time_left // 3600)
                minutes = int((time_left % 3600) // 60)
                await ctx.send(f"⏰ You're tired! Rest for {hours}h {minutes}m before working again.")
            else:
                await ctx.send(f"❌ {reason}")
            return
        
        # Anti-spam check
        if not self.bot.rate_limiter.check_user_limit(user_id, 'work', 1, 3600):
            await ctx.send("⏰ You're working too fast! Take a break.")
            return
        
        # Random job and payment with anti-exploitation
        job = random.choice(self.work_jobs)
        base_payment = random.randint(job["min"], job["max"])
        
        # Calculate work streak with database validation
        work_streak = user_data.get('work_streak', 0)
        
        # Validate streak (prevent manipulation)
        last_work = user_data.get('last_work')
        if last_work:
            try:
                last_work_time = datetime.fromisoformat(last_work)
                hours_since = (datetime.now() - last_work_time).total_seconds() / 3600
                
                # Reset streak if more than 25 hours (allows 1 hour buffer)
                if hours_since > 25:
                    work_streak = 0
                elif hours_since < 0.9:  # Prevent rapid clicking
                    await ctx.send("⏰ You just worked! Wait a bit before working again.")
                    return
            except:
                work_streak = 0
        
        # Calculate payment with diminishing returns to prevent exploitation
        streak_bonus = min(work_streak * 3, 30)  # Max 30 coin bonus, reduced from 50
        fatigue_penalty = max(0, (user_data.get('total_work_sessions', 0) % 20) * 2)  # Fatigue every 20 works
        
        total_payment = max(10, base_payment + streak_bonus - fatigue_penalty)  # Min 10 coins
        
        # Update with atomic transaction
        success, new_balance = self.bot.db.atomic_work_update(user_id, total_payment, work_streak + 1)
        
        if not success:
            await ctx.send("❌ Work failed due to a database error. Please try again.")
            return
        
        embed = discord.Embed(
            title=f"{job['emoji']} Work Complete!",
            description=f"You worked as a **{job['name']}** and earned **{base_payment} coins**!",
            color=discord.Color.green()
        )
        
        if streak_bonus > 0:
            embed.add_field(
                name="🔥 Streak Bonus",
                value=f"+{streak_bonus} coins (Day {work_streak + 1})",
                inline=True
            )
        
        if fatigue_penalty > 0:
            embed.add_field(
                name="😴 Fatigue",
                value=f"-{fatigue_penalty} coins (take breaks!)",
                inline=True
            )
        
        embed.add_field(
            name="💰 Total Earned",
            value=f"{total_payment} coins",
            inline=True
        )
        
        embed.add_field(
            name="🏦 New Balance",
            value=f"{new_balance:,} coins",
            inline=True
        )
        
        await ctx.send(embed=embed)
        
    @commands.command(name='gamble')
    async def gamble(self, ctx, amount: int = None):
        """Gamble coins with various games"""
        if amount is None:
            embed = discord.Embed(
                title="🎲 Gambling Games",
                description="Choose a game to play:",
                color=discord.Color.orange()
            )
            
            embed.add_field(
                name="🎰 Slot Machine",
                value="`!slots <amount>` - Triple match wins big!",
                inline=False
            )
            
            embed.add_field(
                name="🃏 Blackjack",
                value="`!blackjack <amount>` - Beat the dealer!",
                inline=False
            )
            
            embed.add_field(
                name="🎲 Dice Roll",
                value="`!gamble <amount>` - Simple 50/50 chance",
                inline=False
            )
            
            await ctx.send(embed=embed)
            return
            
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
            
        if user_data['coins'] < amount:
            await ctx.send(f"❌ You only have {user_data['coins']} coins!")
            return
            
        # Simple 50/50 gamble
        win = random.random() < 0.45  # Slightly house-favored
        
        if win:
            winnings = int(amount * 1.8)  # 80% profit
            self.bot.db.add_coins(user_id, winnings - amount)
            
            embed = discord.Embed(
                title="🎉 You Won!",
                description=f"You bet {amount} coins and won {winnings} coins!",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="💰 Profit",
                value=f"+{winnings - amount} coins",
                inline=True
            )
        else:
            self.bot.db.spend_coins(user_id, amount)
            
            embed = discord.Embed(
                title="💸 You Lost!",
                description=f"You lost {amount} coins. Better luck next time!",
                color=discord.Color.red()
            )
            
        new_balance = self.bot.db.get_user(user_id)['coins']
        embed.add_field(
            name="🏦 New Balance",
            value=f"{new_balance} coins",
            inline=True
        )
        
        await ctx.send(embed=embed)
        
    @commands.command(name='slots')
    async def slots(self, ctx, amount: int = None):
        """Play slot machine"""
        if amount is None:
            await ctx.send("Usage: `!slots <amount>`")
            return
            
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
            
        if user_data['coins'] < amount:
            await ctx.send(f"❌ You only have {user_data['coins']} coins!")
            return
            
        # Generate slot results
        slots = [random.choice(self.slot_emojis) for _ in range(3)]
        
        # Calculate winnings
        if slots[0] == slots[1] == slots[2]:
            # Triple match
            multiplier = 10 if slots[0] == '💰' else 5
            winnings = amount * multiplier
            self.bot.db.add_coins(user_id, winnings - amount)
            result_text = f"🎰 JACKPOT! Triple {slots[0]}! You won {winnings} coins!"
            color = discord.Color.gold()
        elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
            # Double match
            winnings = amount * 2
            self.bot.db.add_coins(user_id, winnings - amount)
            result_text = f"🎰 Double match! You won {winnings} coins!"
            color = discord.Color.green()
        else:
            # No match
            self.bot.db.spend_coins(user_id, amount)
            result_text = f"🎰 No match. You lost {amount} coins."
            color = discord.Color.red()
            
        embed = discord.Embed(
            title="🎰 Slot Machine",
            description=f"**{slots[0]} | {slots[1]} | {slots[2]}**\n\n{result_text}",
            color=color
        )
        
        new_balance = self.bot.db.get_user(user_id)['coins']
        embed.add_field(
            name="💰 Balance",
            value=f"{new_balance} coins",
            inline=True
        )
        
        await ctx.send(embed=embed)
        
    @commands.command(name='blackjack', aliases=['bj'])
    async def blackjack(self, ctx, amount: int = None):
        """Play blackjack against the bot"""
        if amount is None:
            await ctx.send("Usage: `!blackjack <amount>`")
            return
            
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
            
        if user_data['coins'] < amount:
            await ctx.send(f"❌ You only have {user_data['coins']} coins!")
            return
            
        # Simple blackjack implementation
        deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        random.shuffle(deck)
        
        player_cards = [deck.pop(), deck.pop()]
        dealer_cards = [deck.pop(), deck.pop()]
        
        def card_value(cards):
            total = 0
            aces = 0
            for card in cards:
                if card in ['J', 'Q', 'K']:
                    total += 10
                elif card == 'A':
                    aces += 1
                    total += 11
                else:
                    total += int(card)
            
            while total > 21 and aces > 0:
                total -= 10
                aces -= 1
            return total
        
        player_total = card_value(player_cards)
        dealer_total = card_value(dealer_cards)
        
        embed = discord.Embed(title="🃏 Blackjack", color=discord.Color.blue())
        embed.add_field(
            name="Your Cards",
            value=f"{' '.join(player_cards)} (Total: {player_total})",
            inline=False
        )
        embed.add_field(
            name="Dealer's Cards",
            value=f"{dealer_cards[0]} ❓ (Showing: {card_value([dealer_cards[0]])})",
            inline=False
        )
        
        if player_total == 21:
            # Player blackjack
            winnings = int(amount * 2.5)
            self.bot.db.add_coins(user_id, winnings - amount)
            embed.add_field(name="Result", value=f"🎉 BLACKJACK! You won {winnings} coins!", inline=False)
        elif player_total > 21:
            # Player bust
            self.bot.db.spend_coins(user_id, amount)
            embed.add_field(name="Result", value=f"💥 BUST! You lost {amount} coins.", inline=False)
        else:
            # Dealer plays
            while dealer_total < 17:
                dealer_cards.append(deck.pop())
                dealer_total = card_value(dealer_cards)
            
            embed.set_field_at(1, 
                name="Dealer's Cards",
                value=f"{' '.join(dealer_cards)} (Total: {dealer_total})",
                inline=False
            )
            
            if dealer_total > 21:
                # Dealer bust
                winnings = amount * 2
                self.bot.db.add_coins(user_id, winnings - amount)
                embed.add_field(name="Result", value=f"🎉 Dealer bust! You won {winnings} coins!", inline=False)
            elif player_total > dealer_total:
                # Player wins
                winnings = amount * 2
                self.bot.db.add_coins(user_id, winnings - amount)
                embed.add_field(name="Result", value=f"🎉 You win! You won {winnings} coins!", inline=False)
            elif player_total == dealer_total:
                # Tie
                embed.add_field(name="Result", value=f"🤝 Push! Your {amount} coins are returned.", inline=False)
            else:
                # Dealer wins
                self.bot.db.spend_coins(user_id, amount)
                embed.add_field(name="Result", value=f"😞 Dealer wins. You lost {amount} coins.", inline=False)
        
        new_balance = self.bot.db.get_user(user_id)['coins']
        embed.add_field(name="💰 Balance", value=f"{new_balance} coins", inline=True)
        
        await ctx.send(embed=embed)
        
    @commands.command(name='shop')
    async def shop(self, ctx):
        """View the coin shop"""
        embed = discord.Embed(
            title="🛍️ Coin Shop",
            description="Spend your coins on various items and perks!",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="🎭 Custom Status (500 coins)",
            value="Set a custom status for 24 hours\n`!buy status <message>`",
            inline=False
        )
        
        embed.add_field(
            name="🎨 Profile Color (300 coins)",
            value="Change your embed color for a week\n`!buy color <hex_color>`",
            inline=False
        )
        
        embed.add_field(
            name="💎 VIP Role (1000 coins)",
            value="Get VIP perks for 7 days\n`!buy vip`",
            inline=False
        )
        
        embed.add_field(
            name="🍀 Luck Boost (200 coins)",
            value="Increase gambling luck for 1 hour\n`!buy luck`",
            inline=False
        )
        
        embed.add_field(
            name="⚡ XP Boost (150 coins)",
            value="Double XP for 1 hour\n`!buy xpboost`",
            inline=False
        )
        
        embed.set_footer(text="Use !buy <item> to purchase items")
        
        await ctx.send(embed=embed)
        
    @commands.command(name='buy')
    async def buy(self, ctx, item: str = None, *, args: str = None):
        """Buy items from the shop"""
        if not item:
            await ctx.send("Usage: `!buy <item> [args]`\nUse `!shop` to see available items.")
            return
            
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        shop_items = {
            'status': {'cost': 500, 'name': 'Custom Status'},
            'color': {'cost': 300, 'name': 'Profile Color'},
            'vip': {'cost': 1000, 'name': 'VIP Role'},
            'luck': {'cost': 200, 'name': 'Luck Boost'},
            'xpboost': {'cost': 150, 'name': 'XP Boost'}
        }
        
        if item.lower() not in shop_items:
            await ctx.send(f"❌ Item '{item}' not found! Use `!shop` to see available items.")
            return
            
        shop_item = shop_items[item.lower()]
        cost = shop_item['cost']
        
        if user_data['coins'] < cost:
            await ctx.send(f"❌ You need {cost} coins to buy {shop_item['name']}! You have {user_data['coins']} coins.")
            return
            
        # Process purchase
        self.bot.db.spend_coins(user_id, cost)
        
        # Apply item effects
        current_time = datetime.now()
        user_perks = user_data.get('active_perks', {})
        
        if item.lower() == 'status':
            if not args:
                await ctx.send("❌ Please provide a status message: `!buy status <message>`")
                self.bot.db.add_coins(user_id, cost)  # Refund
                return
            user_perks['custom_status'] = {
                'message': args,
                'expires': (current_time + timedelta(days=1)).isoformat()
            }
            
        elif item.lower() == 'color':
            if not args or not args.startswith('#'):
                await ctx.send("❌ Please provide a hex color: `!buy color #FF0000`")
                self.bot.db.add_coins(user_id, cost)  # Refund
                return
            user_perks['profile_color'] = {
                'color': args,
                'expires': (current_time + timedelta(days=7)).isoformat()
            }
            
        elif item.lower() == 'vip':
            user_perks['vip'] = {
                'expires': (current_time + timedelta(days=7)).isoformat()
            }
            
        elif item.lower() == 'luck':
            user_perks['luck_boost'] = {
                'expires': (current_time + timedelta(hours=1)).isoformat()
            }
            
        elif item.lower() == 'xpboost':
            user_perks['xp_boost'] = {
                'expires': (current_time + timedelta(hours=1)).isoformat()
            }
        
        self.bot.db.update_user_data(user_id, {'active_perks': user_perks})
        
        embed = discord.Embed(
            title="✅ Purchase Successful!",
            description=f"You bought **{shop_item['name']}** for {cost} coins!",
            color=discord.Color.green()
        )
        
        new_balance = self.bot.db.get_user(user_id)['coins']
        embed.add_field(name="💰 Remaining Balance", value=f"{new_balance} coins", inline=True)
        
        await ctx.send(embed=embed)
        
    @commands.command(name='leaderboard', aliases=['lb'])
    async def leaderboard(self, ctx, category: str = 'coins'):
        """Show various leaderboards"""
        valid_categories = ['coins', 'level', 'work', 'gambling']
        
        if category.lower() not in valid_categories:
            embed = discord.Embed(
                title="📊 Leaderboard Categories",
                description="Choose a category:",
                color=discord.Color.blue()
            )
            embed.add_field(name="Available Categories", value="\n".join([f"• `{cat}`" for cat in valid_categories]), inline=False)
            await ctx.send(embed=embed)
            return
            
        # Get top users based on category
        if category.lower() == 'coins':
            top_users = self.bot.db.get_top_users_by_coins(10)
            title = "💰 Richest Users"
            value_key = 'coins'
            value_suffix = ' coins'
        elif category.lower() == 'work':
            top_users = self.bot.db.get_top_users_by_work(10)
            title = "💼 Most Hardworking"
            value_key = 'total_work_sessions'
            value_suffix = ' work sessions'
        else:
            top_users = self.bot.db.get_top_users_by_coins(10)  # Default fallback
            title = "📊 Leaderboard"
            value_key = 'coins'
            value_suffix = ' coins'
            
        if not top_users:
            await ctx.send("❌ No users found for this category.")
            return
            
        embed = discord.Embed(title=title, color=discord.Color.gold())
        
        for i, user_data in enumerate(top_users[:10], 1):
            try:
                user = await self.bot.fetch_user(int(user_data['user_id']))
                name = user.display_name
            except:
                name = f"User {user_data['user_id']}"
                
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            value = user_data.get(value_key, 0)
            
            embed.add_field(
                name=f"{medal} {name}",
                value=f"{value:,}{value_suffix}",
                inline=True
            )
            
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
import discord
from discord.ext import commands
import random
import asyncio
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EconomyCommands(commands.Cog):
    """Economy and game system commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.daily_cooldown = {}  # User cooldowns
        self.work_cooldown = {}
        self.crime_cooldown = {}
        
    @commands.command(name='balance', aliases=['bal', 'coins'])
    async def balance_command(self, ctx, member: discord.Member = None):
        """Check your or someone's balance"""
        target = member or ctx.author
        user_data = self.bot.db.get_user(str(target.id))
        
        embed = discord.Embed(
            title=f"💰 {target.display_name}'s Balance",
            description=f"**{user_data.get('coins', 0):,}** coins",
            color=0x00FF00
        )
        embed.add_field(name="Level", value=user_data.get('level', 1), inline=True)
        embed.add_field(name="XP", value=f"{user_data.get('xp', 0)}/{user_data.get('level', 1) * 100}", inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name='daily')
    async def daily_command(self, ctx):
        """Claim daily coins with exploit protection"""
        user_id = str(ctx.author.id)
        
        # Check if user is banned
        user_data = self.bot.db.get_user(user_id)
        if user_data.get('is_banned', 0):
            await ctx.send("❌ You are banned from using economy commands.")
            return
        
        # Use atomic daily claim system
        success, message, new_balance = self.bot.db.claim_daily(user_id)
        
        if not success:
            await ctx.send(f"❌ {message}")
            return
        
        # Parse streak from message
        streak = 1
        if "streak:" in message.lower():
            try:
                streak = int(message.split("streak: ")[1].split(" ")[0])
            except:
                pass
        
        # Calculate reward from balance change
        daily_amount = 100  # Base amount
        if streak >= 7:
            daily_amount = int(100 * 1.5)
        elif streak >= 3:
            daily_amount = int(100 * 1.2)
        
        embed = discord.Embed(
            title="🎁 Daily Reward Claimed!",
            description=f"You received **{daily_amount}** coins!",
            color=discord.Color.green()
        )
        
        embed.add_field(name="💰 New Balance", value=f"{new_balance:,} coins", inline=True)
        embed.add_field(name="🔥 Daily Streak", value=f"{streak} days", inline=True)
        
        # Add streak bonuses
        if streak >= 7:
            embed.add_field(name="🎉 Bonus", value="🔥 **7-day streak bonus!**", inline=False)
        elif streak >= 3:
            embed.add_field(name="🎉 Bonus", value="⚡ **3-day streak bonus!**", inline=False)
        
        embed.add_field(name="⏰ Next Daily", value="Available in 24 hours", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='work')
    async def work_command(self, ctx):
        """Work to earn coins"""
        user_id = str(ctx.author.id)
        
        # Check cooldown (1 hour)
        if user_id in self.work_cooldown:
            time_left = self.work_cooldown[user_id] - datetime.now()
            if time_left.total_seconds() > 0:
                minutes = int(time_left.total_seconds() // 60)
                await ctx.send(f"⏰ You're tired! Rest for {minutes} more minutes.")
                return
        
        jobs = [
            "programming", "designing", "writing", "streaming", "gaming",
            "teaching", "cooking", "cleaning", "gardening", "studying"
        ]
        
        job = random.choice(jobs)
        earnings = random.randint(50, 200)
        
        self.bot.db.update_user_coins(user_id, earnings)
        self.work_cooldown[user_id] = datetime.now() + timedelta(hours=1)
        
        embed = discord.Embed(
            title="💼 Work Complete",
            description=f"You spent an hour {job} and earned **{earnings:,}** coins!",
            color=0x5865F2
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='crime')
    async def crime_command(self, ctx):
        """Commit crimes for high risk/reward"""
        user_id = str(ctx.author.id)
        
        # Check cooldown (2 hours)
        if user_id in self.crime_cooldown:
            time_left = self.crime_cooldown[user_id] - datetime.now()
            if time_left.total_seconds() > 0:
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                await ctx.send(f"🚔 You're laying low! Wait {hours}h {minutes}m")
                return
        
        crimes = [
            "robbing a bank", "stealing candy", "jaywalking", "littering",
            "pirating movies", "not returning shopping carts", "tax evasion"
        ]
        
        crime = random.choice(crimes)
        success = random.random() > 0.4  # 60% success rate
        
        if success:
            earnings = random.randint(200, 800)
            self.bot.db.update_user_coins(user_id, earnings)
            
            embed = discord.Embed(
                title="🎭 Crime Successful",
                description=f"You got away with {crime} and earned **{earnings:,}** coins!",
                color=0x00FF00
            )
        else:
            fine = random.randint(100, 400)
            self.bot.db.update_user_coins(user_id, -fine)
            
            embed = discord.Embed(
                title="🚔 Crime Failed",
                description=f"You got caught {crime} and paid a **{fine:,}** coin fine!",
                color=0xFF0000
            )
        
        self.crime_cooldown[user_id] = datetime.now() + timedelta(hours=2)
        await ctx.send(embed=embed)
    
    @commands.command(name='shop')
    async def shop_command(self, ctx):
        """View the shop"""
        items = [
            {"name": "Premium Role", "price": 10000, "description": "Get a special role"},
            {"name": "Custom Status", "price": 5000, "description": "Set a custom status"},
            {"name": "Lucky Charm", "price": 2000, "description": "Increases work earnings"},
            {"name": "VIP Access", "price": 15000, "description": "Access to VIP channels"},
            {"name": "Color Change", "price": 3000, "description": "Change your role color"}
        ]
        
        embed = discord.Embed(
            title="🛍️ Shop",
            description="Use `!buy <item>` to purchase items",
            color=0x5865F2
        )
        
        for i, item in enumerate(items, 1):
            embed.add_field(
                name=f"{i}. {item['name']} - {item['price']:,} coins",
                value=item['description'],
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='buy')
    async def buy_command(self, ctx, *, item_name: str):
        """Buy an item from the shop"""
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        items = {
            "premium role": {"price": 10000, "description": "Special role"},
            "custom status": {"price": 5000, "description": "Custom status"},
            "lucky charm": {"price": 2000, "description": "Increases earnings"},
            "vip access": {"price": 15000, "description": "VIP access"},
            "color change": {"price": 3000, "description": "Role color change"}
        }
        
        item = items.get(item_name.lower())
        if not item:
            await ctx.send("❌ Item not found! Check `!shop` for available items.")
            return
        
        if user_data.get('coins', 0) < item['price']:
            await ctx.send(f"💰 You need {item['price']:,} coins but only have {user_data.get('coins', 0):,}!")
            return
        
        # Purchase item
        self.bot.db.update_user_coins(user_id, -item['price'])
        
        # Add to inventory
        inventory = self.bot.db.get_user_data(user_id, 'inventory', [])
        inventory.append(item_name.lower())
        self.bot.db.set_user_data(user_id, 'inventory', inventory)
        
        embed = discord.Embed(
            title="✅ Purchase Successful",
            description=f"You bought **{item_name}** for {item['price']:,} coins!",
            color=0x00FF00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='inventory', aliases=['inv'])
    async def inventory_command(self, ctx):
        """View your inventory"""
        user_id = str(ctx.author.id)
        inventory = self.bot.db.get_user_data(user_id, 'inventory', [])
        
        if not inventory:
            await ctx.send("📦 Your inventory is empty! Visit the `!shop` to buy items.")
            return
        
        embed = discord.Embed(
            title="🎒 Your Inventory",
            description="\n".join([f"• {item.title()}" for item in inventory]),
            color=0x5865F2
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='gamble', aliases=['bet'])
    async def gamble_command(self, ctx, amount: str = None):
        """Gamble your coins with comprehensive validation"""
        user_id = str(ctx.author.id)
        
        # Input validation
        if amount is None:
            await ctx.send("❌ Please specify an amount! Usage: `!gamble <amount>` or `!gamble all`")
            return
        
        # Check if user is banned
        user_data = self.bot.db.get_user(user_id)
        if user_data.get('is_banned', 0):
            await ctx.send("❌ You are banned from using economy commands.")
            return
        
        # Check gambling cooldown (prevent spam)
        can_gamble, reason, time_left = self.bot.db.check_command_cooldown(user_id, 'gamble', 10)  # 10 second cooldown
        if not can_gamble and time_left > 0:
            await ctx.send(f"⏰ Slow down! Wait {time_left} seconds before gambling again.")
            return
        
        # Parse amount with validation
        try:
            if amount.lower() == 'all':
                bet_amount = user_data.get('coins', 0)
                if bet_amount > 10000:  # Max bet limit
                    bet_amount = 10000
                    await ctx.send("⚠️ Maximum bet is 10,000 coins! Betting 10,000 instead.")
            else:
                # Remove common formatting
                amount_clean = amount.replace(',', '').replace('k', '000').replace('m', '000000')
                bet_amount = int(float(amount_clean))
        except (ValueError, OverflowError):
            await ctx.send("❌ Invalid amount! Use a number, 'all', or formats like '1k' or '1.5k'")
            return
        
        # Validate bet amount
        if bet_amount <= 0:
            await ctx.send("❌ You must bet at least 1 coin!")
            return
        
        if bet_amount > 10000:
            await ctx.send("❌ Maximum bet is 10,000 coins!")
            return
        
        current_coins = user_data.get('coins', 0)
        if current_coins < bet_amount:
            await ctx.send(f"💰 You don't have enough coins! You have {current_coins:,}, need {bet_amount:,}")
            return
        
        if bet_amount > current_coins * 0.5 and current_coins > 1000:
            # Warning for high bets
            confirm_msg = await ctx.send(f"⚠️ You're betting {bet_amount:,} coins ({bet_amount/current_coins*100:.1f}% of your balance)!\nReact with ✅ to confirm or ❌ to cancel.")
            await confirm_msg.add_reaction("✅")
            await confirm_msg.add_reaction("❌")
            
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == confirm_msg.id
            
            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                if str(reaction.emoji) == "❌":
                    await ctx.send("❌ Gambling cancelled.")
                    return
            except asyncio.TimeoutError:
                await ctx.send("⏰ Confirmation timed out. Gambling cancelled.")
                return
        
        # House edge and win calculation (45% win rate, slightly house-favored)
        win_chance = 0.44  # Slightly reduced from 0.45
        
        # Atomic gambling transaction
        success, result_message, new_balance = self.bot.db.atomic_gamble(user_id, bet_amount, win_chance)
        
        if not success:
            await ctx.send(f"❌ {result_message}")
            return
        
        # Parse result
        won = "won" in result_message.lower()
        
        if won:
            winnings = bet_amount * 2
            profit = winnings - bet_amount
            
            embed = discord.Embed(
                title="🎉 You Won!",
                description=f"You bet {bet_amount:,} coins and won **{winnings:,}** coins!",
                color=discord.Color.green()
            )
            embed.add_field(name="💰 Profit", value=f"+{profit:,} coins", inline=True)
        else:
            embed = discord.Embed(
                title="💸 You Lost!",
                description=f"You bet {bet_amount:,} coins and lost them all!",
                color=discord.Color.red()
            )
            embed.add_field(name="💸 Loss", value=f"-{bet_amount:,} coins", inline=True)
        
        embed.add_field(name="🏦 New Balance", value=f"{new_balance:,} coins", inline=True)
        
        # Add gambling addiction warning for frequent high bets
        total_gambled_today = self.bot.db.get_user_data(user_id, 'total_gambled_today', 0)
        if total_gambled_today > current_coins * 2:
            embed.add_field(name="⚠️ Gambling Warning", 
                           value="Consider taking a break! Gambling can be addictive.", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard', aliases=['lb', 'rich'])
    async def leaderboard_command(self, ctx):
        """View the richest users"""
        try:
            # Get top 10 users by coins
            top_users = self.bot.db.get_top_users_by_coins(10)
            
            if not top_users:
                await ctx.send("📊 No users found in the leaderboard!")
                return
            
            embed = discord.Embed(
                title="🏆 Coin Leaderboard",
                description="Top 10 richest users",
                color=0xFFD700
            )
            
            for i, (user_id, coins) in enumerate(top_users, 1):
                try:
                    user = self.bot.get_user(int(user_id))
                    username = user.display_name if user else f"User {user_id}"
                    
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                    embed.add_field(
                        name=f"{medal} {username}",
                        value=f"{coins:,} coins",
                        inline=False
                    )
                except:
                    continue
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in leaderboard command: {e}")
            await ctx.send("❌ Error loading leaderboard.")

async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))
