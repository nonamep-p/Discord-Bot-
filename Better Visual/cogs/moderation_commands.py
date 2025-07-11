
import discord
from discord.ext import commands
import asyncio
import time
from datetime import datetime, timedelta
import json

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.muted_users = {}
        self.warns = {}
        self.auto_mod_settings = {
            'spam_detection': True,
            'caps_filter': True,
            'link_filter': False,
            'bad_words_filter': True
        }
        
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        """Kick a member from the server"""
        if not member:
            await ctx.send("❌ Please mention a member to kick!")
            return
            
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't kick someone with equal or higher role!")
            return
            
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Member Kicked",
                description=f"{member.mention} has been kicked",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Failed to kick member: {e}")

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        """Ban a member from the server"""
        if not member:
            await ctx.send("❌ Please mention a member to ban!")
            return
            
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't ban someone with equal or higher role!")
            return
            
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Failed to ban member: {e}")

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_name):
        """Unban a member"""
        banned_users = await ctx.guild.bans()
        
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name.lower() == member_name.lower():
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="✅ Member Unbanned",
                    description=f"{user.mention} has been unbanned",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                return
                
        await ctx.send("❌ User not found in ban list!")

    @commands.command(name='mute')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, duration: int = 60, *, reason="No reason provided"):
        """Mute a member for specified minutes"""
        if not member:
            await ctx.send("❌ Please mention a member to mute!")
            return
            
        # Create muted role if it doesn't exist
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        
        await member.add_roles(muted_role, reason=reason)
        
        # Store mute info
        self.muted_users[member.id] = {
            'until': time.time() + (duration * 60),
            'role': muted_role.id
        }
        
        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"{member.mention} has been muted for {duration} minutes",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)
        
        # Auto unmute
        await asyncio.sleep(duration * 60)
        if member.id in self.muted_users:
            await member.remove_roles(muted_role)
            del self.muted_users[member.id]

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        """Warn a member"""
        if not member:
            await ctx.send("❌ Please mention a member to warn!")
            return
            
        user_id = str(member.id)
        if user_id not in self.warns:
            self.warns[user_id] = []
            
        warn_data = {
            'reason': reason,
            'moderator': str(ctx.author.id),
            'timestamp': datetime.now().isoformat()
        }
        self.warns[user_id].append(warn_data)
        
        embed = discord.Embed(
            title="⚠️ Member Warned",
            description=f"{member.mention} has been warned",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Total Warnings", value=len(self.warns[user_id]), inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='warnings')
    async def warnings(self, ctx, member: discord.Member = None):
        """Check warnings for a member"""
        target = member or ctx.author
        user_id = str(target.id)
        
        if user_id not in self.warns or not self.warns[user_id]:
            await ctx.send(f"✅ {target.display_name} has no warnings!")
            return
            
        embed = discord.Embed(
            title=f"⚠️ Warnings for {target.display_name}",
            description=f"Total warnings: {len(self.warns[user_id])}",
            color=discord.Color.yellow()
        )
        
        for i, warn in enumerate(self.warns[user_id][-5:], 1):  # Show last 5 warnings
            embed.add_field(
                name=f"Warning #{i}",
                value=f"**Reason:** {warn['reason']}\n**Date:** {warn['timestamp'][:10]}",
                inline=False
            )
            
        await ctx.send(embed=embed)

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """Clear messages from channel"""
        if amount > 100:
            await ctx.send("❌ Cannot clear more than 100 messages at once!")
            return
            
        deleted = await ctx.channel.purge(limit=amount + 1)
        
        embed = discord.Embed(
            title="🧹 Messages Cleared",
            description=f"Cleared {len(deleted) - 1} messages",
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        await message.delete()

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
