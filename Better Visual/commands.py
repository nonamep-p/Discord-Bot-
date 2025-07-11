import discord
from discord.ext import commands
import asyncio
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    @discord.ui.button(label="Configuration", style=discord.ButtonStyle.primary, emoji="⚙️")
    async def config_button(self, interaction: discord.Interaction, button: discord.ui.Button):
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

    @discord.ui.button(label="Chat & AI", style=discord.ButtonStyle.success, emoji="💬")
    async def chat_button(self, interaction: discord.Interaction, button: discord.ui.Button):
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

    @discord.ui.button(label="Economy", style=discord.ButtonStyle.secondary, emoji="💰")
    async def economy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
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
            """,
            inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Security", style=discord.ButtonStyle.danger, emoji="🛡️")
    async def security_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🛡️ Security & Protection",
            description="Advanced security features and moderation tools",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Security Commands",
            value="""
            `!security status` - View all security settings
            `!automod toggle` - Enable/disable auto-moderation
            `!antispam <level>` - Set spam protection level
            `!raidmode <on/off>` - Toggle raid protection
            `!lockdown [channel]` - Emergency server lockdown
            `!blocklist add/remove <word>` - Manage word filters
            """,
            inline=False
        )

        embed.add_field(
            name="Protection Features",
            value="""
            🚫 **Anti-spam** - Message frequency monitoring
            🛡️ **Raid protection** - Mass join detection
            🔍 **Content filtering** - Automatic message scanning
            ⚡ **Rate limiting** - API abuse prevention
            🚨 **Emergency systems** - Instant lockdown capabilities
            📊 **Security analytics** - Real-time threat monitoring
            """,
            inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Configuration", style=discord.ButtonStyle.success, emoji="⚙️")
    async def advanced_config_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚙️ Advanced Configuration",
            description="Comprehensive bot customization and settings",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Configuration Commands",
            value="""
            `!config` - Interactive configuration panel
            `!settings view` - View all current settings
            `!prompt set <text>` - Custom personality prompts
            `!settings chat_frequency <rate>` - Conversation participation
            `!settings personality <mode>` - AI personality modes
            `!settings reactions <on/off>` - Emoji reaction toggles
            """,
            inline=False
        )

        embed.add_field(
            name="Customization Options",
            value="""
            🎭 **Custom Prompts** - Personalized AI personality
            💬 **Chat Settings** - Response frequency and patterns
            🎯 **Behavioral Modes** - Mention-only, random chat, adaptive
            🔧 **Feature Toggles** - Enable/disable specific functions
            📊 **Analytics** - Usage tracking and performance metrics
            🌐 **Server-specific** - Different settings per server
            """,
            inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Info & Status", style=discord.ButtonStyle.secondary, emoji="ℹ️")
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="ℹ️ Bot Info & System Status",
            description="Check bot performance, limits, and system information",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Status Commands",
            value="""
            `!ping` - Bot latency and response time
            `!uptime` - How long bot has been running
            `!limits` - API usage and rate limits
            `!status` - Comprehensive system status
            `!version` - Bot version and update info
            """,
            inline=False
        )

        embed.add_field(
            name="System Information",
            value="""
            ⚡ **Performance** - Real-time latency monitoring
            📊 **Usage Stats** - Command usage and analytics
            🔄 **API Limits** - Rate limiting and quota tracking
            💾 **Memory Usage** - System resource monitoring
            🔗 **Connectivity** - Discord API connection status
            📈 **Analytics** - Usage patterns and trends
            """,
            inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

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

            await interaction.response.edit_message(embed=embed, view=self)
            await interaction.message.add_reaction('🎉')
        else:
            embed = discord.Embed(
                title="⏰ Daily Already Claimed",
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

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Back to Balance", style=discord.ButtonStyle.grey)
    async def back_to_balance(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💰 Your Balance",
            description=f"**{self.user_data['coins']}** coins",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📊 Stats",
            value=f"Commands used: {self.user_data.get('total_commands', 0)}",
            inline=True
        )

        embed.set_footer(text="Use !daily to get 100 coins daily!")

        view = BalanceView(self.bot, self.user_data)
        await interaction.response.edit_message(embed=embed, view=view)

class ChatView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    @discord.ui.button(label="Quick Chat", style=discord.ButtonStyle.primary, emoji="💬")
    async def quick_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
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

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Roleplay Mode", style=discord.ButtonStyle.success, emoji="🎭")
    async def roleplay_mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎭 Roleplay Mode",
            description="Use `!roleplay [character]` to switch personalities.\n\nExamples:\n• `!roleplay pirate`\n• `!roleplay wizard`\n• `!roleplay friendly cat`",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="Available Modes",
            value="• Pirate, Wizard, Robot\n• Chef, Detective, Default\n• Or create your own!",
            inline=False
        )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Natural Chat", style=discord.ButtonStyle.secondary, emoji="😊")
    async def natural_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
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

        await interaction.response.edit_message(embed=embed, view=self)

class LimitsView(discord.ui.View):
    def __init__(self, bot, usage_data):
        super().__init__(timeout=300)
        self.bot = bot
        self.usage_data = usage_data

    @discord.ui.button(label="API Calls", style=discord.ButtonStyle.primary, emoji="🔄")
    async def api_calls(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_calls_remaining = max(0, 50 - self.usage_data.get('hourly_calls', 0))

        embed = discord.Embed(
            title="🔄 API Calls (Hourly)",
            description=f"**{api_calls_remaining}/50** calls remaining",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Usage",
            value=f"Used: {self.usage_data.get('hourly_calls', 0)} calls this hour",
            inline=True
        )

        embed.add_field(
            name="Reset",
            value="Resets every hour",
            inline=True
        )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Images", style=discord.ButtonStyle.success, emoji="🎨")
    async def images(self, interaction: discord.Interaction, button: discord.ui.Button):
        images_remaining = max(0, 10 - self.usage_data.get('images_today', 0))

        embed = discord.Embed(
            title="🎨 Images (Daily)",
            description=f"**{images_remaining}/10** images remaining",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Usage",
            value=f"Used: {self.usage_data.get('images_today', 0)} images today",
            inline=True
        )

        embed.add_field(
            name="Reset",
            value="Resets daily at midnight",
            inline=True
        )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Back to Limits", style=discord.ButtonStyle.grey)
    async def back_to_limits(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_calls_remaining = max(0, 50 - self.usage_data.get('hourly_calls', 0))
        images_remaining = max(0, 10 - self.usage_data.get('images_today', 0))

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

        view = LimitsView(self.bot, self.usage_data)
        await interaction.response.edit_message(embed=embed, view=view)

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
            name="✨ Enhanced AI Features",
            value="""
            🤖 **Smart Responses:** Responds to name mentions, DMs, and natural conversation
            🧠 **Memory System:** Remembers chat history and user preferences
            🎭 **Dynamic Personality:** Custom prompts and adaptive personality modes
            🎯 **Configurable Behavior:** Adjustable chat frequency and response patterns
            🛡️ **Security Integration:** Built-in protection and policy compliance
            ⚡ **Real-time Config:** Live settings updates without restart
            """,
            inline=False
        )

        embed.add_field(
            name="💕 Social Commands",
            value="""`!hug <user>` - Hug someone
`!pat <user>` - Pat someone
`!ship <user1> <user2>` - Ship calculator
`!compliment [user]` - Give compliment
`!confession <message>` - Anonymous confession
`!quote` - Inspirational quote
`!marry <user>` - Marriage proposal""",
            inline=False
        )

        # Moderation Commands
        embed.add_field(
            name="🛡️ Moderation Commands",
            value="""`!kick <user>` - Kick a member
`!ban <user>` - Ban a member
`!mute <user> [time]` - Mute a member
`!warn <user>` - Warn a member
`!clear [amount]` - Clear messages
`!lock/unlock` - Lock/unlock channel""",
            inline=False
        )

        # Music Commands
        embed.add_field(
            name="🎵 Music Commands",
            value="""`!play <song>` - Play music
`!skip` - Skip current song
`!queue` - Show music queue
`!stop` - Stop music
`!loop` - Toggle loop mode""",
            inline=False
        )

        # Leveling Commands
        embed.add_field(
            name="📈 Leveling Commands",
            value="""`!rank [user]` - Check XP/level
`!leaderboard` - XP leaderboard
`!givexp <user> <amount>` - Give XP (Admin)""",
            inline=False
        )

        # Fun Commands
        embed.add_field(
            name="🎉 Fun Commands",
            value="""`!truth/dare` - Truth or dare
`!roast <user>` - Friendly roast
`!joke` - Random joke
`!fact` - Random fact
`!rate <thing>` - Rate something
`!choose <options>` - Make a choice""",
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
            embed = discord.Embed(
                title="🎭 Roleplay Mode",
                description="Use `!roleplay [character]` to switch personalities.\n\nExamples:\n• `!roleplay pirate`\n• `!roleplay wizard`\n• `!roleplay friendly cat`",
                color=discord.Color.purple()
            )

            embed.add_field(
                name="Available Modes",
                value="• Pirate, Wizard, Robot\n• Chef, Detective, Default\n• Or create your own!",
                inline=False
            )

            view = ChatView(self.bot)
            await ctx.send(embed=embed, view=view)
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

    @commands.command(name='limits')
    async def limits(self, ctx):
        """Show remaining API limits with interactive buttons"""
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

        view = LimitsView(self.bot, usage_data)
        await ctx.send(embed=embed, view=view)

    @commands.command(name='status')
    async def status(self, ctx):
        """Show detailed bot status"""
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🤖 Bot Status",
            description="Detailed system information",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Connection",
            value=f"Latency: {latency}ms\nStatus: Online",
            inline=True
        )

        embed.add_field(
            name="Servers",
            value=f"Connected to {len(self.bot.guilds)} servers",
            inline=True
        )

        embed.add_field(
            name="Personality",
            value=f"Mode: {self.bot.settings['personality_mode'].title()}\nChat Frequency: {self.bot.settings['chat_frequency'] * 100:.0f}%",
            inline=True
        )

        embed.add_field(
            name="Features",
            value=f"Random Chat: {'✅' if self.bot.settings['random_chat_enabled'] else '❌'}\nReactions: {'✅' if self.bot.settings['reactions_enabled'] else '❌'}",
            inline=True
        )

        await ctx.send(embed=embed)