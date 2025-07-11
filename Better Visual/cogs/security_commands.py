
import discord
from discord.ext import commands
import asyncio
import logging
import time
import json
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SecurityView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Auto Moderation", style=discord.ButtonStyle.danger, emoji="🛡️")
    async def auto_mod_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🛡️ Auto Moderation Settings",
            description="Configure automatic moderation features",
            color=discord.Color.red()
        )
        
        security = self.bot.security_manager
        
        embed.add_field(
            name="Current Settings",
            value=f"""
            **Anti-Spam:** {'✅ Enabled' if security.anti_spam_enabled else '❌ Disabled'}
            **Bad Words Filter:** {'✅ Enabled' if security.bad_words_filter else '❌ Disabled'}
            **Link Protection:** {'✅ Enabled' if security.link_protection else '❌ Disabled'}
            **Raid Protection:** {'✅ Enabled' if security.raid_protection else '❌ Disabled'}
            **NSFW Detection:** {'✅ Enabled' if security.nsfw_detection else '❌ Disabled'}
            **Mass Mention Protection:** {'✅ Enabled' if security.mass_mention_protection else '❌ Disabled'}
            """,
            inline=False
        )
        
        view = AutoModerationView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
        
    @discord.ui.button(label="User Management", style=discord.ButtonStyle.primary, emoji="👥")
    async def user_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="👥 User Management",
            description="Manage users, timeouts, and permissions",
            color=discord.Color.blue()
        )
        
        security = self.bot.security_manager
        
        embed.add_field(
            name="Statistics",
            value=f"""
            **Blocked Users:** {len(security.blocked_users)}
            **Warned Users:** {len(security.warned_users)}
            **Trusted Users:** {len(security.trusted_users)}
            **Quarantined Users:** {len(security.quarantined_users)}
            """,
            inline=False
        )
        
        view = UserManagementView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
        
    @discord.ui.button(label="Content Filter", style=discord.ButtonStyle.secondary, emoji="🔍")
    async def content_filter(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔍 Content Filtering",
            description="Configure message and content filtering",
            color=discord.Color.purple()
        )
        
        security = self.bot.security_manager
        
        embed.add_field(
            name="Filter Settings",
            value=f"""
            **Profanity Level:** {security.profanity_level}/5
            **URL Whitelist:** {len(security.allowed_domains)} domains
            **Blocked Words:** {len(security.blocked_words)} words
            **File Types:** {len(security.allowed_file_types)} allowed
            **Max Message Length:** {security.max_message_length}
            **Image Scanning:** {'✅ Enabled' if security.image_scanning else '❌ Disabled'}
            """,
            inline=False
        )
        
        view = ContentFilterView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
        
    @discord.ui.button(label="Security Logs", style=discord.ButtonStyle.success, emoji="📋")
    async def security_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📋 Security Logs",
            description="View recent security events and alerts",
            color=discord.Color.green()
        )
        
        security = self.bot.security_manager
        recent_logs = security.get_recent_logs(limit=10)
        
        if recent_logs:
            log_text = ""
            for log in recent_logs:
                log_text += f"• **{log['type']}** - {log['description'][:50]}...\n"
            embed.add_field(name="Recent Events", value=log_text, inline=False)
        else:
            embed.add_field(name="Recent Events", value="No recent security events", inline=False)
        
        view = SecurityLogsView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class AutoModerationView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Toggle Anti-Spam", style=discord.ButtonStyle.primary)
    async def toggle_antispam(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        security.anti_spam_enabled = not security.anti_spam_enabled
        status = "Enabled" if security.anti_spam_enabled else "Disabled"
        
        embed = discord.Embed(
            title="✅ Anti-Spam Updated",
            description=f"Anti-spam protection {status}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Configure Raid Protection", style=discord.ButtonStyle.danger)
    async def configure_raid(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🚨 Raid Protection Configuration",
            description="Configure automatic raid detection and response",
            color=discord.Color.red()
        )
        
        security = self.bot.security_manager
        embed.add_field(
            name="Current Settings",
            value=f"""
            **Join Rate Limit:** {security.join_rate_limit} users/minute
            **Auto Lockdown:** {'✅ Enabled' if security.auto_lockdown else '❌ Disabled'}
            **Suspicious Account Age:** {security.min_account_age} days
            **Auto Ban New Accounts:** {'✅ Enabled' if security.auto_ban_new_accounts else '❌ Disabled'}
            """,
            inline=False
        )
        
        view = RaidProtectionView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
        
    @discord.ui.button(label="NSFW Detection", style=discord.ButtonStyle.secondary)
    async def nsfw_detection(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        security.nsfw_detection = not security.nsfw_detection
        status = "Enabled" if security.nsfw_detection else "Disabled"
        
        embed = discord.Embed(
            title="✅ NSFW Detection Updated",
            description=f"NSFW content detection {status}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back", style=discord.ButtonStyle.grey)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Security Configuration",
            description="Configure comprehensive security settings",
            color=discord.Color.red()
        )
        view = SecurityView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class UserManagementView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="View Blocked Users", style=discord.ButtonStyle.danger)
    async def view_blocked(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        blocked_users = list(security.blocked_users)[:10]  # Show first 10
        
        embed = discord.Embed(
            title="🚫 Blocked Users",
            description=f"Showing {len(blocked_users)} of {len(security.blocked_users)} blocked users",
            color=discord.Color.red()
        )
        
        if blocked_users:
            user_list = ""
            for user_id in blocked_users:
                try:
                    user = self.bot.get_user(int(user_id))
                    user_list += f"• {user.mention if user else f'ID: {user_id}'}\n"
                except:
                    user_list += f"• ID: {user_id}\n"
            embed.add_field(name="Blocked Users", value=user_list, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Trusted Users", style=discord.ButtonStyle.success)
    async def view_trusted(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        trusted_users = list(security.trusted_users)[:10]
        
        embed = discord.Embed(
            title="✅ Trusted Users",
            description=f"Showing {len(trusted_users)} of {len(security.trusted_users)} trusted users",
            color=discord.Color.green()
        )
        
        if trusted_users:
            user_list = ""
            for user_id in trusted_users:
                try:
                    user = self.bot.get_user(int(user_id))
                    user_list += f"• {user.mention if user else f'ID: {user_id}'}\n"
                except:
                    user_list += f"• ID: {user_id}\n"
            embed.add_field(name="Trusted Users", value=user_list, inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back", style=discord.ButtonStyle.grey)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Security Configuration",
            description="Configure comprehensive security settings",
            color=discord.Color.red()
        )
        view = SecurityView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class ContentFilterView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Adjust Profanity Level", style=discord.ButtonStyle.primary)
    async def adjust_profanity(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        security.profanity_level = (security.profanity_level % 5) + 1
        
        levels = {
            1: "Very Lenient",
            2: "Lenient", 
            3: "Moderate",
            4: "Strict",
            5: "Very Strict"
        }
        
        embed = discord.Embed(
            title="✅ Profanity Filter Updated",
            description=f"Profanity level set to {security.profanity_level}/5 ({levels[security.profanity_level]})",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Toggle Image Scanning", style=discord.ButtonStyle.secondary)
    async def toggle_image_scan(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        security.image_scanning = not security.image_scanning
        status = "Enabled" if security.image_scanning else "Disabled"
        
        embed = discord.Embed(
            title="✅ Image Scanning Updated",
            description=f"Image content scanning {status}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back", style=discord.ButtonStyle.grey)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Security Configuration",
            description="Configure comprehensive security settings",
            color=discord.Color.red()
        )
        view = SecurityView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class RaidProtectionView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Increase Join Rate", style=discord.ButtonStyle.primary)
    async def increase_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        security.join_rate_limit = min(20, security.join_rate_limit + 2)
        
        embed = discord.Embed(
            title="✅ Join Rate Updated",
            description=f"Join rate limit set to {security.join_rate_limit} users/minute",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Decrease Join Rate", style=discord.ButtonStyle.danger)
    async def decrease_rate(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        security.join_rate_limit = max(2, security.join_rate_limit - 2)
        
        embed = discord.Embed(
            title="✅ Join Rate Updated",
            description=f"Join rate limit set to {security.join_rate_limit} users/minute",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Toggle Auto Lockdown", style=discord.ButtonStyle.secondary)
    async def toggle_lockdown(self, interaction: discord.Interaction, button: discord.ui.Button):
        security = self.bot.security_manager
        security.auto_lockdown = not security.auto_lockdown
        status = "Enabled" if security.auto_lockdown else "Disabled"
        
        embed = discord.Embed(
            title="✅ Auto Lockdown Updated",
            description=f"Automatic server lockdown {status}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)

class SecurityLogsView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Clear Logs", style=discord.ButtonStyle.danger)
    async def clear_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.security_manager.clear_logs()
        
        embed = discord.Embed(
            title="✅ Logs Cleared",
            description="All security logs have been cleared",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Export Logs", style=discord.ButtonStyle.primary)
    async def export_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        logs = self.bot.security_manager.get_all_logs()
        
        if logs:
            log_data = json.dumps(logs, indent=2)
            file = discord.File(
                filename="security_logs.json",
                fp=io.BytesIO(log_data.encode())
            )
            
            embed = discord.Embed(
                title="📄 Security Logs Export",
                description="Security logs have been exported",
                color=discord.Color.blue()
            )
            
            await interaction.response.edit_message(embed=embed, view=self)
            await interaction.followup.send(file=file, ephemeral=True)
        else:
            embed = discord.Embed(
                title="❌ No Logs",
                description="No security logs to export",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=self)

class SecurityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="security", description="Access security configuration panel")
    @commands.has_permissions(administrator=True)
    async def security_config(self, ctx):
        """Comprehensive security configuration panel"""
        embed = discord.Embed(
            title="🔒 Advanced Security System",
            description="Configure comprehensive bot security features",
            color=discord.Color.red()
        )
        
        security = self.bot.security_manager
        
        embed.add_field(
            name="🛡️ Protection Status",
            value=f"""
            **Auto Moderation:** {'🟢 Active' if security.anti_spam_enabled else '🔴 Inactive'}
            **Raid Protection:** {'🟢 Active' if security.raid_protection else '🔴 Inactive'}
            **Content Filter:** {'🟢 Active' if security.bad_words_filter else '🔴 Inactive'}
            **NSFW Detection:** {'🟢 Active' if security.nsfw_detection else '🔴 Inactive'}
            """,
            inline=True
        )
        
        embed.add_field(
            name="📊 Statistics",
            value=f"""
            **Blocked Users:** {len(security.blocked_users)}
            **Security Events:** {len(security.security_logs)}
            **Trusted Users:** {len(security.trusted_users)}
            **Warnings Issued:** {security.warnings_issued}
            """,
            inline=True
        )
        
        embed.add_field(
            name="⚙️ Configuration",
            value="Use the buttons below to configure security settings",
            inline=False
        )
        
        view = SecurityView(self.bot)
        await ctx.send(embed=embed, view=view)
        
    @commands.command(name="block")
    @commands.has_permissions(moderate_members=True)
    async def block_user(self, ctx, user: discord.User, *, reason="No reason provided"):
        """Block a user from using the bot"""
        self.bot.security_manager.block_user(str(user.id), reason, ctx.author.id)
        
        embed = discord.Embed(
            title="🚫 User Blocked",
            description=f"{user.mention} has been blocked from using the bot",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        
    @commands.command(name="unblock")
    @commands.has_permissions(moderate_members=True)
    async def unblock_user(self, ctx, user: discord.User):
        """Unblock a user"""
        self.bot.security_manager.unblock_user(str(user.id))
        
        embed = discord.Embed(
            title="✅ User Unblocked",
            description=f"{user.mention} has been unblocked",
            color=discord.Color.green()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        
    @commands.command(name="trust")
    @commands.has_permissions(administrator=True)
    async def trust_user(self, ctx, user: discord.User):
        """Add user to trusted list (bypasses some restrictions)"""
        self.bot.security_manager.add_trusted_user(str(user.id))
        
        embed = discord.Embed(
            title="✅ User Trusted",
            description=f"{user.mention} has been added to the trusted users list",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
    @commands.command(name="untrust")
    @commands.has_permissions(administrator=True)
    async def untrust_user(self, ctx, user: discord.User):
        """Remove user from trusted list"""
        self.bot.security_manager.remove_trusted_user(str(user.id))
        
        embed = discord.Embed(
            title="✅ User Untrusted",
            description=f"{user.mention} has been removed from the trusted users list",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SecurityCommands(bot))
