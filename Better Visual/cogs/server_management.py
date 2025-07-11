
import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime

class ServerManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_settings = {}
        self.auto_roles = {}
        self.reaction_roles = {}

    @commands.command(name='setwelcome')
    @commands.has_permissions(manage_guild=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel = None, *, message=None):
        """Set welcome message and channel"""
        if not channel:
            await ctx.send("❌ Please specify a channel!\nExample: `!setwelcome #general Welcome {user}!`")
            return
            
        if not message:
            message = "Welcome to {server}, {user}! 🎉"
            
        self.welcome_settings[ctx.guild.id] = {
            'channel_id': channel.id,
            'message': message
        }
        
        embed = discord.Embed(
            title="✅ Welcome Message Set",
            description=f"Welcome messages will be sent to {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Message Preview", value=message.format(user="@NewUser", server=ctx.guild.name), inline=False)
        embed.add_field(name="Variables", value="`{user}` - Mentions the new user\n`{server}` - Server name", inline=False)
        
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message when someone joins"""
        guild_id = member.guild.id
        
        if guild_id in self.welcome_settings:
            settings = self.welcome_settings[guild_id]
            channel = member.guild.get_channel(settings['channel_id'])
            
            if channel:
                message = settings['message'].format(
                    user=member.mention,
                    server=member.guild.name
                )
                
                embed = discord.Embed(
                    title="👋 Welcome!",
                    description=message,
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
                embed.add_field(name="Member Count", value=f"{member.guild.member_count} members", inline=True)
                
                await channel.send(embed=embed)
        
        # Auto roles
        if guild_id in self.auto_roles:
            role_ids = self.auto_roles[guild_id]
            for role_id in role_ids:
                role = member.guild.get_role(role_id)
                if role:
                    try:
                        await member.add_roles(role)
                    except:
                        pass

    @commands.command(name='setautorole')
    @commands.has_permissions(manage_roles=True)
    async def set_auto_role(self, ctx, role: discord.Role):
        """Set a role to be automatically given to new members"""
        if ctx.guild.id not in self.auto_roles:
            self.auto_roles[ctx.guild.id] = []
            
        if role.id not in self.auto_roles[ctx.guild.id]:
            self.auto_roles[ctx.guild.id].append(role.id)
            
            embed = discord.Embed(
                title="✅ Auto Role Added",
                description=f"New members will automatically receive {role.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ {role.mention} is already an auto role!")

    @commands.command(name='removeautorole')
    @commands.has_permissions(manage_roles=True)
    async def remove_auto_role(self, ctx, role: discord.Role):
        """Remove an auto role"""
        if ctx.guild.id in self.auto_roles and role.id in self.auto_roles[ctx.guild.id]:
            self.auto_roles[ctx.guild.id].remove(role.id)
            
            embed = discord.Embed(
                title="✅ Auto Role Removed",
                description=f"{role.mention} will no longer be given to new members",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ {role.mention} is not an auto role!")

    @commands.command(name='reactionrole')
    @commands.has_permissions(manage_roles=True)
    async def reaction_role(self, ctx, message_id: int, emoji, role: discord.Role):
        """Set up reaction roles"""
        try:
            message = await ctx.channel.fetch_message(message_id)
        except:
            await ctx.send("❌ Message not found in this channel!")
            return
            
        # Add reaction to message
        try:
            await message.add_reaction(emoji)
        except:
            await ctx.send("❌ Invalid emoji!")
            return
            
        # Store reaction role data
        if ctx.guild.id not in self.reaction_roles:
            self.reaction_roles[ctx.guild.id] = {}
            
        if message_id not in self.reaction_roles[ctx.guild.id]:
            self.reaction_roles[ctx.guild.id][message_id] = {}
            
        self.reaction_roles[ctx.guild.id][message_id][str(emoji)] = role.id
        
        embed = discord.Embed(
            title="✅ Reaction Role Set",
            description=f"Users can react with {emoji} to get {role.mention}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle reaction role assignment"""
        if user.bot:
            return
            
        guild_id = reaction.message.guild.id
        message_id = reaction.message.id
        emoji = str(reaction.emoji)
        
        if (guild_id in self.reaction_roles and 
            message_id in self.reaction_roles[guild_id] and 
            emoji in self.reaction_roles[guild_id][message_id]):
            
            role_id = self.reaction_roles[guild_id][message_id][emoji]
            role = reaction.message.guild.get_role(role_id)
            
            if role and role not in user.roles:
                try:
                    await user.add_roles(role)
                except:
                    pass

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        """Handle reaction role removal"""
        if user.bot:
            return
            
        guild_id = reaction.message.guild.id
        message_id = reaction.message.id
        emoji = str(reaction.emoji)
        
        if (guild_id in self.reaction_roles and 
            message_id in self.reaction_roles[guild_id] and 
            emoji in self.reaction_roles[guild_id][message_id]):
            
            role_id = self.reaction_roles[guild_id][message_id][emoji]
            role = reaction.message.guild.get_role(role_id)
            
            if role and role in user.roles:
                try:
                    await user.remove_roles(role)
                except:
                    pass

    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Set slowmode for the channel"""
        if seconds < 0 or seconds > 21600:  # Max 6 hours
            await ctx.send("❌ Slowmode must be between 0 and 21600 seconds (6 hours)!")
            return
            
        await ctx.channel.edit(slowmode_delay=seconds)
        
        if seconds == 0:
            embed = discord.Embed(
                title="✅ Slowmode Disabled",
                description="Slowmode has been turned off for this channel",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="✅ Slowmode Enabled",
                description=f"Slowmode set to {seconds} seconds for this channel",
                color=discord.Color.blue()
            )
            
        await ctx.send(embed=embed)

    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Lock a channel"""
        channel = channel or ctx.channel
        
        overwrites = channel.overwrites_for(ctx.guild.default_role)
        overwrites.send_messages = False
        
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        
        embed = discord.Embed(
            title="🔒 Channel Locked",
            description=f"{channel.mention} has been locked",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unlock a channel"""
        channel = channel or ctx.channel
        
        overwrites = channel.overwrites_for(ctx.guild.default_role)
        overwrites.send_messages = True
        
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        
        embed = discord.Embed(
            title="🔓 Channel Unlocked",
            description=f"{channel.mention} has been unlocked",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerManagementCog(bot))
