import discord
from discord.ext import commands
import datetime

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bothelp')
    async def bothelp(self, ctx):
        """Show all available commands"""
        embed = discord.Embed(
            title="🤖 Kaala Billota - Advanced Discord Bot",
            description="🎯 **Natural Chat AI** • 🛡️ **Security Features** • ⚙️ **Full Configuration**\n\nHere are all available commands:",
            color=discord.Color.gold()
        )
        
        # AI & Chat Commands
        embed.add_field(
            name="🤖 AI & Chat Commands",
            value="""`!chat <message>` - Chat with AI using current persona
`!image <prompt>` - Generate image using DeepSeek
`!persona [name]` - Switch AI persona or list available personas
`!prompt set <text>` - Set custom personality prompt
`!prompt clear` - Remove custom prompt
`!prompt show` - View current prompt""",
            inline=False
        )
        
        # Configuration Commands
        embed.add_field(
            name="⚙️ Configuration Commands",
            value="""`!config` - Interactive configuration panel
`!settings view` - View all current settings
`!settings chat_frequency <0.0-1.0>` - Set chat participation rate
`!settings personality <mode>` - Change personality mode
`!settings reactions <on/off>` - Toggle emoji reactions""",
            inline=False
        )
        
        # Security Commands
        embed.add_field(
            name="🛡️ Security & Moderation",
            value="""`!security status` - View security settings
`!automod toggle` - Enable/disable automod
`!antispam <level>` - Set anti-spam level
`!blocklist add/remove <word>` - Manage blocked words
`!raidmode <on/off>` - Toggle raid protection
`!lockdown [channel]` - Emergency lockdown""",
            inline=False
        )
        
        # Game Commands
        embed.add_field(
            name="🎮 Interactive Games",
            value="""`!trivia` - Answer trivia questions
`!wordle` - Play Wordle game
`!rps <choice>` - Rock Paper Scissors
`!8ball <question>` - Magic 8-ball
`!guess` - Number guessing game
`!mathchallenge` - Solve math problems
`!wordgame` - Word association game""",
            inline=False
        )
        
        # Economy System
        embed.add_field(
            name="💰 Economy System",
            value="""`!balance` - Check coin balance
`!daily` - Claim daily coins (100 coins)
`!work` - Work for coins (1hr cooldown)
`!gamble <amount>` - Gamble coins
`!shop` - View coin shop
`!gift <user> <amount>` - Give coins to someone
`!leaderboard` - Top coin holders""",
            inline=False
        )
        
        # Social Features
        embed.add_field(
            name="💕 Social & Fun",
            value="""`!hug/pat/kiss <user>` - Social interactions
`!ship <user1> <user2>` - Compatibility calculator
`!compliment [user]` - Give/receive compliments
`!confession <message>` - Anonymous confessions
`!quote` - Inspirational quotes
`!marry <user>` - Marriage system
`!divorce` - End marriage
`!profile [user]` - View user profile""",
            inline=False
        )
        
        # Entertainment & Mini Games
        embed.add_field(
            name="🎮 Mini Games & Entertainment",
            value="""`!hangman` - Word guessing game
`!connect4 <user>` - Connect 4 with someone
`!tictactoe <user>` - Tic Tac Toe game
`!snake` - Snake game with reactions
`!riddle` - Solve riddles
`!poll <question> <options>` - Create polls
`!fortune` - Fortune cookie messages
`!moodmeter [user]` - Check mood level
`!advice` - Get life advice""",
            inline=False
        )
        
        # Fun Commands
        embed.add_field(
            name="🎭 Fun & Social",
            value="""`!truth` - Truth questions
`!dare` - Dare challenges
`!roast <user>` - Friendly roasts
`!fact` - Random facts
`!joke` - Tell jokes
`!wouldyourather` - Would you rather
`!rate <thing>` - Rate something 1-10
`!choose <options>` - Choose between options
`!coinflip` - Flip a coin
`!dice [sides]` - Roll dice""",
            inline=False
        )
        
        # Advanced Utilities
        embed.add_field(
            name="🔧 Advanced Utilities",
            value="""`!remind <time> <message>` - Set reminders
`!translate <lang> <text>` - Translate text
`!weather <location>` - Weather info
`!reactionrole <msg_id> <emoji> <role>` - Set reaction roles
`!autoresponse <trigger> <response>` - Auto responses
`!setwelcome <channel> <message>` - Welcome messages""",
            inline=False
        )
        
        # Server Management
        embed.add_field(
            name="🛠️ Server & Info",
            value="""`!ping` - Bot latency
`!uptime` - Bot uptime
`!serverinfo` - Server information
`!userinfo [user]` - User information
`!limits` - API usage info
`!status` - System status""",
            inline=False
        )
        
        # Natural Features
        embed.add_field(
            name="✨ Natural AI Features",
            value="""🔹 **Responds to:** bilota, billota, kaala, @mentions, DMs
🔹 **Smart conversation** with memory and context
🔹 **Personality shifting** based on conversation
🔹 **Random chat participation** (configurable)
🔹 **Human-like responses** with natural delays
🔹 **Emoji reactions** and engaging interactions""",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ Security Features",
            value="""🔒 **Anti-spam protection** • 🚫 **Raid detection**
⚡ **Rate limiting** • 🔍 **Message filtering**
🛡️ **Auto-moderation** • 🚨 **Emergency lockdown**""",
            inline=False
        )
        
        embed.set_footer(text="💡 Tip: Use !config for interactive setup • !security status for protection info")
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        """Get information about the server"""
        guild = ctx.guild
        
        # Count channels by type
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        # Count members
        total_members = guild.member_count
        online_members = len([m for m in guild.members if m.status != discord.Status.offline])
        
        embed = discord.Embed(
            title=f"📊 {guild.name} Server Info",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="👑 Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        
        embed.add_field(name="👥 Members", value=f"{online_members}/{total_members} online", inline=True)
        embed.add_field(name="📝 Text Channels", value=text_channels, inline=True)
        embed.add_field(name="🔊 Voice Channels", value=voice_channels, inline=True)
        
        embed.add_field(name="📂 Categories", value=categories, inline=True)
        embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        await ctx.send(embed=embed)

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get information about a user"""
        member = member or ctx.author
        
        # Get user roles (excluding @everyone)
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        roles.reverse()  # Show highest role first
        
        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color
        )
        
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        
        embed.add_field(name="🎭 Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name="🔰 Roles", value=" ".join(roles[:10]) if roles else "None", inline=False)
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
            
        await ctx.send(embed=embed)

    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Show bot uptime"""
        uptime = datetime.datetime.utcnow() - self.bot.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        embed = discord.Embed(
            title="⏰ Bot Uptime",
            description=f"🕐 {days}d {hours}h {minutes}m {seconds}s",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
