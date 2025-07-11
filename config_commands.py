import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import logging

logger = logging.getLogger(__name__)

class ConfigView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Chat Settings", style=discord.ButtonStyle.primary, emoji="💬")
    async def chat_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="💬 Chat Configuration",
            description="Configure how I interact in conversations",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Current Settings",
            value=f"""
            **Chat Frequency:** {self.bot.settings['chat_frequency'] * 100}%
            **Random Chat:** {'✅ Enabled' if self.bot.settings['random_chat_enabled'] else '❌ Disabled'}
            **Mention Only:** {'✅ Enabled' if self.bot.settings['mention_only'] else '❌ Disabled'}
            **Reactions:** {'✅ Enabled' if self.bot.settings['reactions_enabled'] else '❌ Disabled'}
            """,
            inline=False
        )
        
        view = ChatSettingsView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
        
    @discord.ui.button(label="Personality", style=discord.ButtonStyle.success, emoji="🎭")
    async def personality_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎭 Personality Configuration",
            description="Choose how I behave and respond",
            color=discord.Color.green()
        )
        
        personalities = {
            'friendly': '😊 Warm and approachable',
            'witty': '😄 Clever and humorous',
            'casual': '😌 Relaxed and informal',
            'enthusiastic': '🎉 Energetic and excited',
            'thoughtful': '🤔 Deep and reflective'
        }
        
        current = self.bot.settings['personality_mode']
        embed.add_field(
            name="Current Personality",
            value=f"**{current.title()}** - {personalities.get(current, 'Custom')}",
            inline=False
        )
        
        embed.add_field(
            name="Available Personalities",
            value="\n".join([f"• **{k.title()}** - {v}" for k, v in personalities.items()]),
            inline=False
        )
        
        view = PersonalityView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
        
    @discord.ui.button(label="Features", style=discord.ButtonStyle.secondary, emoji="⚙️")
    async def feature_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚙️ Feature Configuration",
            description="Enable or disable bot features",
            color=discord.Color.orange()
        )
        
        embed.add_field(
            name="Current Features",
            value=f"""
            **Natural Chat:** {'✅ Enabled' if self.bot.settings['random_chat_enabled'] else '❌ Disabled'}
            **Reactions:** {'✅ Enabled' if self.bot.settings['reactions_enabled'] else '❌ Disabled'}
            **Memory:** ✅ Enabled
            **Personality Shifts:** ✅ Enabled
            """,
            inline=False
        )
        
        view = FeatureView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class ChatSettingsView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Increase Frequency", style=discord.ButtonStyle.primary)
    async def increase_freq(self, interaction: discord.Interaction, button: discord.ui.Button):
        current = self.bot.settings['chat_frequency']
        new_freq = min(0.5, current + 0.05)
        self.bot.settings['chat_frequency'] = new_freq
        
        embed = discord.Embed(
            title="✅ Chat Frequency Updated",
            description=f"Chat frequency increased to {new_freq * 100:.0f}%",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Decrease Frequency", style=discord.ButtonStyle.danger)
    async def decrease_freq(self, interaction: discord.Interaction, button: discord.ui.Button):
        current = self.bot.settings['chat_frequency']
        new_freq = max(0.01, current - 0.05)
        self.bot.settings['chat_frequency'] = new_freq
        
        embed = discord.Embed(
            title="✅ Chat Frequency Updated",
            description=f"Chat frequency decreased to {new_freq * 100:.0f}%",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Toggle Random Chat", style=discord.ButtonStyle.secondary)
    async def toggle_random(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.settings['random_chat_enabled'] = not self.bot.settings['random_chat_enabled']
        status = "Enabled" if self.bot.settings['random_chat_enabled'] else "Disabled"
        
        embed = discord.Embed(
            title="✅ Random Chat Updated",
            description=f"Random chat {status}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back", style=discord.ButtonStyle.grey)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="�� Bot Configuration",
            description="Choose what you'd like to configure:",
            color=discord.Color.blue()
        )
        view = ConfigView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class PersonalityView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Friendly", style=discord.ButtonStyle.primary, emoji="😊")
    async def friendly(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.settings['personality_mode'] = 'friendly'
        embed = discord.Embed(
            title="✅ Personality Updated",
            description="I'm now in **Friendly** mode - warm and approachable! 😊",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Witty", style=discord.ButtonStyle.success, emoji="😄")
    async def witty(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.settings['personality_mode'] = 'witty'
        embed = discord.Embed(
            title="✅ Personality Updated",
            description="I'm now in **Witty** mode - clever and humorous! 😄",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Casual", style=discord.ButtonStyle.secondary, emoji="😌")
    async def casual(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.settings['personality_mode'] = 'casual'
        embed = discord.Embed(
            title="✅ Personality Updated",
            description="I'm now in **Casual** mode - relaxed and informal! 😌",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back", style=discord.ButtonStyle.grey)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="�� Bot Configuration",
            description="Choose what you'd like to configure:",
            color=discord.Color.blue()
        )
        view = ConfigView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class FeatureView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Toggle Reactions", style=discord.ButtonStyle.primary)
    async def toggle_reactions(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.settings['reactions_enabled'] = not self.bot.settings['reactions_enabled']
        status = "Enabled" if self.bot.settings['reactions_enabled'] else "Disabled"
        
        embed = discord.Embed(
            title="✅ Reactions Updated",
            description=f"Reactions {status}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Back", style=discord.ButtonStyle.grey)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🤖 Bot Configuration",
            description="Choose what you'd like to configure:",
            color=discord.Color.blue()
        )
        view = ConfigView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class ConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="config", description="Configure bot settings")
    async def config(self, interaction: discord.Interaction):
        """Interactive configuration panel"""
        embed = discord.Embed(
            title="🤖 Bot Configuration",
            description="Choose what you'd like to configure:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Current Status",
            value=f"""
            **Personality:** {self.bot.settings['personality_mode'].title()}
            **Chat Frequency:** {self.bot.settings['chat_frequency'] * 100:.0f}%
            **Random Chat:** {'✅' if self.bot.settings['random_chat_enabled'] else '❌'}
            **Reactions:** {'✅' if self.bot.settings['reactions_enabled'] else '❌'}
            """,
            inline=False
        )
        
        view = ConfigView(self.bot)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))
