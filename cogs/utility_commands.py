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
            title="🤖 Discord AI Bot Commands",
            description="Here are all the available commands:",
            color=discord.Color.blue()
        )
        
        # AI Commands
        embed.add_field(
            name="🤖 AI Commands",
            value="""`!chat <message>` - Chat with AI using current persona
`!image <prompt>` - Generate image using DeepSeek
`!persona [name]` - Switch AI persona or list available personas""",
            inline=False
        )
        
        # Media Commands
        embed.add_field(
            name="🎬 Media Commands",
            value="""`!gif <search>` - Search for GIFs
`!meme` - Get a random meme""",
            inline=False
        )
        
        # Utility Commands
        embed.add_field(
            name="🔧 Utility Commands",
            value="""`!ping` - Check bot latency
`!serverinfo` - Get server information
`!userinfo [user]` - Get user information
`!bothelp` - Show this help message""",
            inline=False
        )
        
        embed.set_footer(text="Use !bothelp for detailed information about commands")
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
