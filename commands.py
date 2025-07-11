import discord
from discord.ext import commands
import asyncio
import logging
import random
from datetime import datetime, timedelta, timezone
import json

logger = logging.getLogger(__name__)

class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Configuration", style=discord.ButtonStyle.primary, emoji="⚙️")
    async def config_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="⚙️ Configuration Commands",
                description="Manage bot settings and behavior",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Commands",
                value="""
                `!config` - Interactive configuration panel
                `!help` - Show this help menu
                """,
                inline=False
            )
            
            embed.add_field(
                name="Features",
                value="""
                • Adjust chat frequency
                • Change personality modes
                • Toggle reactions and features
                • Real-time settings updates
                """,
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error loading configuration info!", ephemeral=True)
        
    @discord.ui.button(label="Chat & AI", style=discord.ButtonStyle.success, emoji="💬")
    async def chat_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="💬 Chat & AI Commands",
                description="Interact with the AI and manage conversations",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Commands",
                value="""
                `!chat [message]` - Direct AI chat (10 coins)
                `!roleplay [character]` - Switch personality mode
                `!transactions` - View your transaction history
                """,
                inline=False
            )
            
            embed.add_field(
                name="Natural Features",
                value="""
                • Responds to name: **bilota**, **billota**, **kaala**
                • Joins conversations randomly
                • Remembers chat history
                • Personality shifts based on conversation
                """,
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error loading chat info!", ephemeral=True)
        
    @discord.ui.button(label="Economy", style=discord.ButtonStyle.secondary, emoji="💰")
    async def economy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="💰 Economy Commands",
                description="Manage your coins and rewards",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="Commands",
                value="""
                `!balance` - Check your coins
                `!daily` - Get daily reward (100 coins)
                `!gift [user] [amount]` - Give coins to someone
                `!transactions` - View transaction history
                """,
                inline=False
            )
            
            embed.add_field(
                name="Features",
                value="""
                • Daily coin rewards
                • Gift system for sharing
                • Coin-based command costs
                • Balance tracking
                • Transaction history
                """,
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error loading economy info!", ephemeral=True)
        
    @discord.ui.button(label="Info & Status", style=discord.ButtonStyle.danger, emoji="ℹ️")
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="ℹ️ Info & Status Commands",
                description="Check bot status and limits",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="Commands",
                value="""
                `!ping` - Check bot latency
                `!limits` - Show API usage limits
                `!status` - Bot status and uptime
                """,
                inline=False
            )
            
            embed.add_field(
                name="Features",
                value="""
                • Real-time latency monitoring
                • API usage tracking
                • Rate limit information
                • System status updates
                • Usage progress bars
                """,
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error loading status info!", ephemeral=True)
    
    @discord.ui.button(label="Back to Help", style=discord.ButtonStyle.grey)
    async def back_to_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="🤖 Kaala Billota - Interactive Help",
                description="Choose a category to explore commands and features:",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="✨ Natural Features",
                value="""
                • I respond when you call my name: **bilota**, **billota**, **kaala**
                • I respond to mentions and DMs
                • I join conversations randomly (configurable)
                • I remember our chat history
                • I can change personality based on conversation
                • I add reactions and use emojis naturally
                """,
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error returning to help menu!", ephemeral=True)

class BalanceView(discord.ui.View):
    def __init__(self, bot, user_data):
        super().__init__(timeout=300)
        self.bot = bot
        self.user_data = user_data
        
    @discord.ui.button(label="Claim Daily", style=discord.ButtonStyle.success, emoji="🎁")
    async def claim_daily(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        
        if self.bot.db.can_claim_daily(user_id):
            new_balance = self.bot.db.claim_daily(user_id)
            
            embed = discord.Embed(
                title="🎁 Daily Reward Claimed!",
                description=f"You received **100 coins**!\nNew balance: **{new_balance}** coins",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="⏰ Next Daily",
                value="Available in 24 hours",
                inline=True
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
            await interaction.message.add_reaction('🎉')
        else:
            # Calculate time until next daily
            user_data = self.bot.db.get_user(user_id)
            if user_data.get('last_daily'):
                last_daily = datetime.fromisoformat(user_data['last_daily'])
                next_daily = last_daily + timedelta(days=1)
                time_remaining = next_daily - datetime.now(timezone.utc)
                
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                
                embed = discord.Embed(
                    title="⏰ Daily Reward Already Claimed",
                    description="You've already claimed your daily reward today!",
                    color=discord.Color.orange()
                )
                
                embed.add_field(
                    name="⏳ Time Remaining",
                    value=f"{hours}h {minutes}m until next daily",
                    inline=True
                )
                
                await interaction.response.edit_message(embed=embed, view=self)
            else:
                embed = discord.Embed(
                    title="⏰ Daily Reward Already Claimed",
                    description="You've already claimed your daily reward today!\nCome back tomorrow for more coins.",
                    color=discord.Color.orange()
                )
                
                await interaction.response.edit_message(embed=embed, view=self)
            
    @discord.ui.button(label="Gift Coins", style=discord.ButtonStyle.primary, emoji="💝")
    async def gift_coins(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💝 Gift Coins",
            description="Use `!gift @user amount` to gift coins to someone.\n\nExample: `!gift @friend 50`",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="Your Balance",
            value=f"**{self.user_data['coins']}** coins available",
            inline=True
        )
        
        embed.add_field(
            name="Transaction History",
            value="Use `!transactions` to see your recent activity",
            inline=True
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back to Balance", style=discord.ButtonStyle.grey)
    async def back_to_balance(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Refresh user data
        user_id = str(interaction.user.id)
        user_data = self.bot.db.get_user(user_id)
        self.user_data = user_data
        
        # Get recent transaction history
        transactions = self.bot.db.get_transaction_history(user_id, 3)
        
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
        
        # Add recent transactions if any
        if transactions:
            recent_transactions = []
            for tx in transactions[:3]:
                if tx['type'] == 'daily_reward':
                    recent_transactions.append(f"🎁 Daily reward: +{tx['amount']}")
                elif tx['type'] == 'spend':
                    recent_transactions.append(f"💬 Chat cost: {tx['amount']}")
                elif tx['type'] == 'transfer_sent':
                    recent_transactions.append(f"💝 Gift sent: {tx['amount']}")
                elif tx['type'] == 'transfer_received':
                    recent_transactions.append(f"🎁 Gift received: +{tx['amount']}")
            
            if recent_transactions:
                embed.add_field(
                    name="📈 Recent Activity",
                    value="\n".join(recent_transactions),
                    inline=False
                )
        
        embed.set_footer(text="Use the buttons below to manage your coins!")
        
        await interaction.response.edit_message(embed=embed, view=self)

class ChatView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Quick Chat", style=discord.ButtonStyle.primary, emoji="💬")
    async def quick_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="💬 Quick Chat",
                description="Use `!chat [message]` to start a conversation.\n\nExample: `!chat Hello, how are you?`",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Cost",
                value="10 coins per chat",
                inline=True
            )
            
            embed.add_field(
                name="Features",
                value="• AI-powered responses\n• Conversation memory\n• Personality modes",
                inline=True
            )
            
            embed.add_field(
                name="💡 Tip",
                value="You can also just mention me or call my name to chat naturally!",
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error loading chat info!", ephemeral=True)
        
    @discord.ui.button(label="Roleplay Mode", style=discord.ButtonStyle.success, emoji="🎭")
    async def roleplay_mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="🎭 Roleplay Mode",
                description="Use `!roleplay [character]` to switch personalities.\n\n**Available Characters:**",
                color=discord.Color.purple()
            )
            
            # Get available personalities
            available_personalities = self.bot.personality.get_available_personalities()
            basic_personalities = ['friendly', 'witty', 'casual', 'enthusiastic', 'thoughtful']
            roleplay_personalities = ['pirate', 'wizard', 'robot', 'chef', 'detective']
            
            basic_desc = "\n".join([f"• **{p.title()}**" for p in basic_personalities if p in available_personalities])
            roleplay_desc = "\n".join([f"• **{p.title()}**" for p in roleplay_personalities if p in available_personalities])
            
            embed.add_field(
                name="😊 Basic Personalities",
                value=basic_desc,
                inline=False
            )
            
            embed.add_field(
                name="🎭 Roleplay Characters",
                value=roleplay_desc,
                inline=False
            )
            
            embed.add_field(
                name="💡 Examples",
                value="`!roleplay pirate` • `!roleplay wizard` • `!roleplay robot`",
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error loading roleplay info!", ephemeral=True)
        
    @discord.ui.button(label="Natural Chat", style=discord.ButtonStyle.secondary, emoji="😊")
    async def natural_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="😊 Natural Conversation",
                description="I respond naturally to messages! Try:\n\n• Call my name: **bilota**, **billota**, **kaala**\n• Mention me: @bot\n• DM me directly\n• I'll join conversations randomly",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Features",
                value="• No commands needed\n• Personality shifts\n• Conversation memory\n• Natural reactions",
                inline=False
            )
            
            embed.add_field(
                name="⚙️ Settings",
                value="Use `!config` to adjust how often I join conversations",
                inline=False
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            await interaction.response.send_message("❌ Error loading natural chat info!", ephemeral=True)
    
    @discord.ui.button(label="Back to Help", style=discord.ButtonStyle.grey)
    async def back_to_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="🤖 Kaala Billota - Interactive Help",
                description="Choose a category to explore commands and features:",
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name="✨ Natural Features",
                value="""
                • I respond when you call my name: **bilota**, **billota**, **kaala**
                • I respond to mentions and DMs
                • I join conversations randomly (configurable)
                • I remember our chat history
                • I can change personality based on conversation
                • I add reactions and use emojis naturally
                """,
                inline=False
            )
            
            view = HelpView(self.bot)
            await interaction.response.edit_message(embed=embed, view=view)
        except Exception as e:
            await interaction.response.send_message("❌ Error returning to help menu!", ephemeral=True)

class LimitsView(discord.ui.View):
    def __init__(self, bot, usage_info):
        super().__init__(timeout=300)
        self.bot = bot
        self.usage_info = usage_info
        
    @discord.ui.button(label="API Calls", style=discord.ButtonStyle.primary, emoji="🔄")
    async def api_calls(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_info = self.usage_info.get('api_calls', {})
        remaining = api_info.get('remaining', 0)
        used = api_info.get('used', 0)
        limit = api_info.get('limit', 50)
        
        embed = discord.Embed(
            title="🔄 API Calls (Hourly)",
            description=f"**{remaining}/{limit}** calls remaining",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Usage",
            value=f"Used: {used} calls this hour",
            inline=True
        )
        
        embed.add_field(
            name="Reset",
            value=api_info.get('reset_time', 'Every hour'),
            inline=True
        )
        
        # Add usage bar
        usage_percentage = (used / limit) * 100
        bar_length = 10
        filled_length = int((usage_percentage / 100) * bar_length)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        embed.add_field(
            name="Progress",
            value=f"`{bar}` {usage_percentage:.1f}%",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Images", style=discord.ButtonStyle.success, emoji="🎨")
    async def images(self, interaction: discord.Interaction, button: discord.ui.Button):
        image_info = self.usage_info.get('images', {})
        remaining = image_info.get('remaining', 0)
        used = image_info.get('used', 0)
        limit = image_info.get('limit', 10)
        
        embed = discord.Embed(
            title="🎨 Images (Daily)",
            description=f"**{remaining}/{limit}** images remaining",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Usage",
            value=f"Used: {used} images today",
            inline=True
        )
        
        embed.add_field(
            name="Reset",
            value=image_info.get('reset_time', 'Daily at midnight'),
            inline=True
        )
        
        # Add usage bar
        usage_percentage = (used / limit) * 100
        bar_length = 10
        filled_length = int((usage_percentage / 100) * bar_length)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        embed.add_field(
            name="Progress",
            value=f"`{bar}` {usage_percentage:.1f}%",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back to Limits", style=discord.ButtonStyle.grey)
    async def back_to_limits(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📊 Your Usage Limits",
            description="Here are your remaining limits for today:",
            color=discord.Color.blue()
        )
        
        # API Calls
        api_info = self.usage_info.get('api_calls', {})
        embed.add_field(
            name="🔄 API Calls (Hourly)",
            value=f"**{api_info.get('remaining', 0)}/{api_info.get('limit', 50)}** remaining\nUsed: {api_info.get('used', 0)} calls",
            inline=True
        )
        
        # Images
        image_info = self.usage_info.get('images', {})
        embed.add_field(
            name="🎨 Images (Daily)", 
            value=f"**{image_info.get('remaining', 0)}/{image_info.get('limit', 10)}** remaining\nUsed: {image_info.get('used', 0)} images",
            inline=True
        )
        
        embed.add_field(
            name="📅 Reset Times",
            value=f"• API calls: {api_info.get('reset_time', 'Every hour')}\n• Images: {image_info.get('reset_time', 'Daily at midnight')}",
            inline=False
        )
        
        # Add usage tips
        if api_info.get('remaining', 0) <= 5:
            embed.add_field(
                name="⚠️ Low API Calls",
                value="You're running low on API calls! Consider waiting for the reset.",
                inline=False
            )
        
        if image_info.get('remaining', 0) <= 2:
            embed.add_field(
                name="⚠️ Low Image Credits",
                value="You're running low on image generation credits!",
                inline=False
            )
        
        await interaction.response.edit_message(embed=embed, view=self)

class BotCommands(commands.Cog):
    """All bot commands with interactive buttons"""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show all available commands with interactive buttons"""
        embed = discord.Embed(
            title="🤖 Kaala Billota - Interactive Help",
            description="Choose a category to explore commands and features:",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="✨ Natural Features",
            value="""
            • I respond when you call my name: **bilota**, **billota**, **kaala**
            • I respond to mentions and DMs
            • I join conversations randomly (configurable)
            • I remember our chat history
            • I can change personality based on conversation
            • I add reactions and use emojis naturally
            """,
            inline=False
        )
        
        view = HelpView(self.bot)
        await ctx.send(embed=embed, view=view)
        
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check bot status and latency"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot is online and responsive!\n**Latency:** {latency}ms",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Status",
            value="✅ Online and ready",
            inline=True
        )
        
        embed.add_field(
            name="Uptime",
            value="24/7 Active",
            inline=True
        )
        
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('🏓')
        
    @commands.command(name='balance')
    async def balance(self, ctx):
        """Check user's coin balance with interactive buttons"""
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        # Get recent transaction history
        transactions = self.bot.db.get_transaction_history(user_id, 3)
        
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
        
        # Add recent transactions if any
        if transactions:
            recent_transactions = []
            for tx in transactions[:3]:
                if tx['type'] == 'daily_reward':
                    recent_transactions.append(f"🎁 Daily reward: +{tx['amount']}")
                elif tx['type'] == 'spend':
                    recent_transactions.append(f"💬 Chat cost: {tx['amount']}")
                elif tx['type'] == 'transfer_sent':
                    recent_transactions.append(f"💝 Gift sent: {tx['amount']}")
                elif tx['type'] == 'transfer_received':
                    recent_transactions.append(f"🎁 Gift received: +{tx['amount']}")
            
            if recent_transactions:
                embed.add_field(
                    name="📈 Recent Activity",
                    value="\n".join(recent_transactions),
                    inline=False
                )
        
        embed.set_footer(text="Use the buttons below to manage your coins!")
        
        view = BalanceView(self.bot, user_data)
        await ctx.send(embed=embed, view=view)
        
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
            
            embed.add_field(
                name="⏰ Next Daily",
                value="Available in 24 hours",
                inline=True
            )
            
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('🎉')
        else:
            # Calculate time until next daily
            user_data = self.bot.db.get_user(user_id)
            if user_data.get('last_daily'):
                last_daily = datetime.fromisoformat(user_data['last_daily'])
                next_daily = last_daily + timedelta(days=1)
                time_remaining = next_daily - datetime.now(timezone.utc)
                
                hours = int(time_remaining.total_seconds() // 3600)
                minutes = int((time_remaining.total_seconds() % 3600) // 60)
                
                embed = discord.Embed(
                    title="⏰ Daily Reward Already Claimed",
                    description="You've already claimed your daily reward today!",
                    color=discord.Color.orange()
                )
                
                embed.add_field(
                    name="⏳ Time Remaining",
                    value=f"{hours}h {minutes}m until next daily",
                    inline=True
                )
                
                await ctx.send(embed=embed)
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
            embed = discord.Embed(
                title="❌ Invalid Amount",
                description="Amount must be positive!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
            
        if user == ctx.author:
            embed = discord.Embed(
                title="❌ Invalid Target",
                description="You can't gift coins to yourself!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
            
        sender_id = str(ctx.author.id)
        receiver_id = str(user.id)
        
        # Check if sender has enough coins
        sender_data = self.bot.db.get_user(sender_id)
        if sender_data['coins'] < amount:
            embed = discord.Embed(
                title="❌ Insufficient Coins",
                description=f"You only have **{sender_data['coins']}** coins, but you're trying to gift **{amount}** coins.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return
        
        if self.bot.db.transfer_coins(sender_id, receiver_id, amount):
            sender_balance = self.bot.db.get_user(sender_id)['coins']
            receiver_balance = self.bot.db.get_user(receiver_id)['coins']
            
            embed = discord.Embed(
                title="🎁 Coins Gifted!",
                description=f"{ctx.author.mention} gifted **{amount} coins** to {user.mention}!",
                color=discord.Color.green()
            )
            
            embed.add_field(name="Your new balance", value=f"{sender_balance} coins", inline=True)
            embed.add_field(name=f"{user.display_name}'s balance", value=f"{receiver_balance} coins", inline=True)
            
            await ctx.send(embed=embed)
            await ctx.message.add_reaction('💝')
        else:
            embed = discord.Embed(
                title="❌ Transfer Failed",
                description="The coin transfer failed. Please try again.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
    @commands.command(name='transactions')
    async def transactions(self, ctx):
        """Show recent transaction history"""
        user_id = str(ctx.author.id)
        transactions = self.bot.db.get_transaction_history(user_id, 10)
        
        if not transactions:
            embed = discord.Embed(
                title="📊 Transaction History",
                description="No transactions found.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="📊 Recent Transactions",
            description="Your last 10 transactions:",
            color=discord.Color.blue()
        )
        
        for tx in transactions:
            timestamp = datetime.fromisoformat(tx['timestamp']).strftime("%m/%d %H:%M")
            
            if tx['type'] == 'daily_reward':
                embed.add_field(
                    name=f"🎁 Daily Reward ({timestamp})",
                    value=f"+{tx['amount']} coins • Balance: {tx['balance_after']}",
                    inline=False
                )
            elif tx['type'] == 'spend':
                embed.add_field(
                    name=f"💬 Chat Cost ({timestamp})",
                    value=f"{tx['amount']} coins • Balance: {tx['balance_after']}",
                    inline=False
                )
            elif tx['type'] == 'transfer_sent':
                embed.add_field(
                    name=f"💝 Gift Sent ({timestamp})",
                    value=f"{tx['amount']} coins • Balance: {tx['balance_after']}",
                    inline=False
                )
            elif tx['type'] == 'transfer_received':
                embed.add_field(
                    name=f"🎁 Gift Received ({timestamp})",
                    value=f"+{tx['amount']} coins • Balance: {tx['balance_after']}",
                    inline=False
                )
        
        await ctx.send(embed=embed)
            
    @commands.command(name='chat')
    async def chat(self, ctx, *, message: str = None):
        """Direct AI chat"""
        if not message:
            embed = discord.Embed(
                title="💬 Chat Command",
                description="Use `!chat [message]` to start a conversation.\n\nExample: `!chat Hello, how are you?`",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Cost",
                value="10 coins per chat",
                inline=True
            )
            
            embed.add_field(
                name="Features",
                value="• AI-powered responses\n• Conversation memory\n• Personality modes",
                inline=True
            )
            
            view = ChatView(self.bot)
            await ctx.send(embed=embed, view=view)
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
            response = self.bot.personality.generate_response(
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
            # Show available personalities
            available_personalities = self.bot.personality.get_available_personalities()
            
            embed = discord.Embed(
                title="🎭 Roleplay Mode",
                description="Use `!roleplay [character]` to switch personalities.\n\n**Available Personalities:**",
                color=discord.Color.purple()
            )
            
            # Group personalities by category
            basic_personalities = ['friendly', 'witty', 'casual', 'enthusiastic', 'thoughtful']
            roleplay_personalities = ['pirate', 'wizard', 'robot', 'chef', 'detective']
            
            basic_desc = "\n".join([f"• **{p.title()}** - {self.bot.personality.get_personality_description(p)}" for p in basic_personalities])
            roleplay_desc = "\n".join([f"• **{p.title()}** - {self.bot.personality.get_personality_description(p)}" for p in roleplay_personalities])
            
            embed.add_field(
                name="😊 Basic Personalities",
                value=basic_desc,
                inline=False
            )
            
            embed.add_field(
                name="🎭 Roleplay Characters",
                value=roleplay_desc,
                inline=False
            )
            
            embed.add_field(
                name="💡 Custom Prompts",
                value="Use `!prompt set <your prompt>` to create your own personality!",
                inline=False
            )
            
            view = ChatView(self.bot)
            await ctx.send(embed=embed, view=view)
            return
            
        user_id = str(ctx.author.id)
        character_lower = character.lower()
        
        # Validate personality mode
        if not self.bot.personality.validate_personality_mode(character_lower):
            embed = discord.Embed(
                title="❌ Invalid Personality",
                description=f"'{character}' is not a valid personality mode.",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="Available Personalities",
                value="Use `!roleplay` to see all available options",
                inline=False
            )
            
            await ctx.send(embed=embed)
            return
        
        # Set personality mode in database
        self.bot.db.set_personality_mode(user_id, character_lower)
        
        # Get personality description
        description = self.bot.personality.get_personality_description(character_lower)
        
        embed = discord.Embed(
            title="🎭 Roleplay Mode Activated!",
            description=f"I'm now roleplaying as: **{character.title()}**\n\n{description}",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="💬 How to Use",
            value="I'll respond as this character in our conversations!\nYou can also use `!chat [message]` for direct AI chat.",
            inline=False
        )
        
        embed.add_field(
            name="🔄 Switch Again",
            value="Use `!roleplay [new_character]` to switch to a different personality",
            inline=False
        )
        
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('🎭')
        
    @commands.command(name='limits')
    async def limits(self, ctx):
        """Show remaining API limits with interactive buttons"""
        user_id = str(ctx.author.id)
        usage_info = self.bot.rate_limiter.get_usage_info(user_id)
        
        embed = discord.Embed(
            title="📊 Your Usage Limits",
            description="Here are your remaining limits for today:",
            color=discord.Color.blue()
        )
        
        # API Calls
        api_info = usage_info.get('api_calls', {})
        embed.add_field(
            name="🔄 API Calls (Hourly)",
            value=f"**{api_info.get('remaining', 0)}/{api_info.get('limit', 50)}** remaining\nUsed: {api_info.get('used', 0)} calls",
            inline=True
        )
        
        # Images
        image_info = usage_info.get('images', {})
        embed.add_field(
            name="🎨 Images (Daily)", 
            value=f"**{image_info.get('remaining', 0)}/{image_info.get('limit', 10)}** remaining\nUsed: {image_info.get('used', 0)} images",
            inline=True
        )
        
        embed.add_field(
            name="📅 Reset Times",
            value=f"• API calls: {api_info.get('reset_time', 'Every hour')}\n• Images: {image_info.get('reset_time', 'Daily at midnight')}",
            inline=False
        )
        
        # Add usage tips
        if api_info.get('remaining', 0) <= 5:
            embed.add_field(
                name="⚠️ Low API Calls",
                value="You're running low on API calls! Consider waiting for the reset.",
                inline=False
            )
        
        if image_info.get('remaining', 0) <= 2:
            embed.add_field(
                name="⚠️ Low Image Credits",
                value="You're running low on image generation credits!",
                inline=False
            )
        
        view = LimitsView(self.bot, usage_info)
        await ctx.send(embed=embed, view=view)
        
    @commands.command(name='status')
    async def status(self, ctx):
        """Show detailed bot status and system information"""
        try:
            # Get bot latency
            latency = round(self.bot.latency * 1000)
            
            # Get guild count
            guild_count = len(self.bot.guilds)
            
            # Get user count
            user_count = len(self.bot.users)
            
            # Get uptime
            uptime = datetime.now() - self.bot.start_time if hasattr(self.bot, 'start_time') else timedelta(0)
            hours, remainder = divmod(int(uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            
            embed = discord.Embed(
                title="🤖 Bot Status & Statistics",
                description="Detailed system information and statistics",
                color=discord.Color.blue()
            )
            
            # System Status
            embed.add_field(
                name="🟢 System Status",
                value=f"**Online** • Latency: {latency}ms",
                inline=True
            )
            
            embed.add_field(
                name="⏰ Uptime",
                value=f"{days}d {hours}h {minutes}m {seconds}s",
                inline=True
            )
            
            embed.add_field(
                name="📊 Statistics",
                value=f"**{guild_count}** servers • **{user_count}** users",
                inline=True
            )
            
            # Bot Settings
            embed.add_field(
                name="⚙️ Current Settings",
                value=f"""
                **Chat Frequency:** {self.bot.settings['chat_frequency'] * 100:.0f}%
                **Personality:** {self.bot.settings['personality_mode'].title()}
                **Random Chat:** {'✅' if self.bot.settings['random_chat_enabled'] else '❌'}
                **Reactions:** {'✅' if self.bot.settings['reactions_enabled'] else '❌'}
                """,
                inline=False
            )
            
            # Memory Usage (if available)
            try:
                import psutil
                process = psutil.Process()
                memory_mb = process.memory_info().rss / 1024 / 1024
                cpu_percent = process.cpu_percent()
                
                embed.add_field(
                    name="💾 System Resources",
                    value=f"**Memory:** {memory_mb:.1f} MB\n**CPU:** {cpu_percent:.1f}%",
                    inline=True
                )
            except ImportError:
                pass
            
            # Version Info
            embed.add_field(
                name="📋 Version Info",
                value=f"**Bot:** {self.bot.config.get('version', '2.0.0')}\n**Discord.py:** {discord.__version__}",
                inline=True
            )
            
            embed.set_footer(text="Use !config to adjust settings")
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to get status: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.command(name='stats')
    async def stats(self, ctx):
        """Show user statistics and usage information"""
        try:
            user_id = str(ctx.author.id)
            user_data = self.bot.db.get_user(user_id)
            usage_info = self.bot.rate_limiter.get_usage_info(user_id)
            transactions = self.bot.db.get_transaction_history(user_id, 5)
            
            embed = discord.Embed(
                title="📊 Your Statistics",
                description=f"Personal statistics for {ctx.author.display_name}",
                color=discord.Color.blue()
            )
            
            # Economy Stats
            embed.add_field(
                name="💰 Economy",
                value=f"""
                **Balance:** {user_data['coins']} coins
                **Total Commands:** {user_data.get('total_commands', 0)}
                **Account Created:** {user_data.get('created_at', 'Unknown')[:10]}
                """,
                inline=False
            )
            
            # Usage Stats
            api_info = usage_info.get('api_calls', {})
            image_info = usage_info.get('images', {})
            
            embed.add_field(
                name="📈 Usage This Period",
                value=f"""
                **API Calls:** {api_info.get('used', 0)}/{api_info.get('limit', 50)}
                **Images:** {image_info.get('used', 0)}/{image_info.get('limit', 10)}
                """,
                inline=True
            )
            
            # Recent Activity
            if transactions:
                recent_activity = []
                for tx in transactions[:3]:
                    if tx['type'] == 'daily_reward':
                        recent_activity.append(f"🎁 Daily reward: +{tx['amount']}")
                    elif tx['type'] == 'spend':
                        recent_activity.append(f"💬 Chat: {tx['amount']}")
                    elif tx['type'] == 'transfer_sent':
                        recent_activity.append(f"💝 Gift: {tx['amount']}")
                    elif tx['type'] == 'transfer_received':
                        recent_activity.append(f"🎁 Received: +{tx['amount']}")
                
                if recent_activity:
                    embed.add_field(
                        name="📋 Recent Activity",
                        value="\n".join(recent_activity),
                        inline=False
                    )
            
            embed.set_footer(text="Use !transactions for full history")
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to get statistics: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.command(name='reset')
    async def reset_data(self, ctx):
        """Reset your user data (use with caution)"""
        embed = discord.Embed(
            title="⚠️ Reset User Data",
            description="This will reset your coins, conversation history, and settings to defaults.\n\n**This action cannot be undone!**",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="What will be reset:",
            value="• Coin balance (back to 1000)\n• Conversation history\n• Personality mode\n• Usage statistics",
            inline=False
        )
        
        embed.add_field(
            name="What will be kept:",
            value="• Custom prompts\n• Transaction history",
            inline=False
        )
        
        embed.set_footer(text="Type '!reset confirm' to proceed")
        await ctx.send(embed=embed)
    
    @commands.command(name='reset', hidden=True)
    async def reset_confirm(self, ctx, confirmation: str = None):
        """Confirm reset of user data"""
        if confirmation != "confirm":
            await ctx.send("❌ Reset cancelled. Use `!reset confirm` to proceed.")
            return
        
        try:
            user_id = str(ctx.author.id)
            
            # Reset user data in database
            self.bot.db.reset_user_data(user_id)
            
            embed = discord.Embed(
                title="✅ Data Reset Complete",
                description="Your user data has been reset to defaults.",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Reset Items",
                value="• Coin balance: 1000\n• Conversation history: Cleared\n• Personality mode: Friendly\n• Usage statistics: Reset",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Reset Failed",
                description=f"Error resetting data: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.command(name='backup')
    async def backup_data(self, ctx):
        """Create a backup of your data"""
        try:
            user_id = str(ctx.author.id)
            user_data = self.bot.db.get_user(user_id)
            transactions = self.bot.db.get_transaction_history(user_id, 50)
            conversations = self.bot.db.get_conversation_history(user_id, 20)
            
            backup_data = {
                'user_data': user_data,
                'transactions': transactions,
                'conversations': conversations,
                'backup_date': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            # Create backup file
            backup_filename = f"backup_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(backup_filename, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            embed = discord.Embed(
                title="✅ Backup Created",
                description=f"Your data has been backed up to `{backup_filename}`",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Backup Contents",
                value=f"• User data\n• {len(transactions)} transactions\n• {len(conversations)} conversations",
                inline=False
            )
            
            embed.add_field(
                name="📁 File",
                value=f"`{backup_filename}`",
                inline=True
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Backup Failed",
                description=f"Error creating backup: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """Show top users by coin balance"""
        try:
            # Get top users from database
            top_users = self.bot.db.get_top_users(10)
            
            if not top_users:
                embed = discord.Embed(
                    title="📊 Leaderboard",
                    description="No users found.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(
                title="🏆 Coin Leaderboard",
                description="Top users by coin balance",
                color=discord.Color.gold()
            )
            
            for i, user_data in enumerate(top_users, 1):
                user_id = user_data['user_id']
                coins = user_data['coins']
                
                # Try to get user mention
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    user_display = user.display_name
                except:
                    user_display = f"User {user_id}"
                
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                
                embed.add_field(
                    name=f"{medal} {user_display}",
                    value=f"**{coins:,}** coins",
                    inline=True
                )
            
            embed.set_footer(text="Updated in real-time")
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to load leaderboard: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
