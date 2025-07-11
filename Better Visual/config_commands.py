import discord
from discord.ext import commands
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
        
    @discord.ui.button(label="Custom Prompt", style=discord.ButtonStyle.secondary, emoji="✏️")
    async def custom_prompt_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="✏️ Custom Prompt Configuration",
            description="Set your own personality prompt for the bot",
            color=discord.Color.purple()
        )
        
        # Get current custom prompt
        current_prompt = self.bot.personality.get_custom_prompt(
            str(interaction.user.id),
            str(interaction.guild.id) if interaction.guild else None
        )
        
        embed.add_field(
            name="Current Custom Prompt",
            value=current_prompt[:200] + "..." if current_prompt and len(current_prompt) > 200 else (current_prompt or "None set (using default personality)"),
            inline=False
        )
        
        embed.add_field(
            name="How to Use",
            value="Use `!prompt set <your prompt>` to set a custom personality\nUse `!prompt clear` to remove it",
            inline=False
        )
        
        view = CustomPromptView(self.bot)
        await interaction.response.edit_message(embed=embed, view=view)
        
    @discord.ui.button(label="Security", style=discord.ButtonStyle.danger, emoji="🔒")
    async def security_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Security Settings",
            description="Quick access to security configuration",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="Security Status",
            value="Use `!security` for comprehensive security management",
            inline=False
        )
        
        embed.add_field(
            name="Policy Compliance",
            value="✅ Discord ToS Compliant\n✅ Privacy Protected\n✅ Content Filtered",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
        
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
            **Custom Prompts:** {'✅ Enabled' if self.bot.settings['custom_prompt_enabled'] else '❌ Disabled'}
            **Security:** ✅ Enabled
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
        self.bot.config.set('chat_frequency', new_freq)
        
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
        self.bot.config.set('chat_frequency', new_freq)
        
        embed = discord.Embed(
            title="✅ Chat Frequency Updated",
            description=f"Chat frequency decreased to {new_freq * 100:.0f}%",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Toggle Random Chat", style=discord.ButtonStyle.secondary)
    async def toggle_random(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_value = not self.bot.settings['random_chat_enabled']
        self.bot.settings['random_chat_enabled'] = new_value
        self.bot.config.set('random_chat_enabled', new_value)
        status = "Enabled" if new_value else "Disabled"
        
        embed = discord.Embed(
            title="✅ Random Chat Updated",
            description=f"Random chat {status}",
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
        
    @discord.ui.button(label="Enthusiastic", style=discord.ButtonStyle.danger, emoji="🎉")
    async def enthusiastic(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.settings['personality_mode'] = 'enthusiastic'
        embed = discord.Embed(
            title="✅ Personality Updated",
            description="I'm now in **Enthusiastic** mode - energetic and excited! 🎉",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Thoughtful", style=discord.ButtonStyle.primary, emoji="🤔")
    async def thoughtful(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.settings['personality_mode'] = 'thoughtful'
        embed = discord.Embed(
            title="✅ Personality Updated",
            description="I'm now in **Thoughtful** mode - deep and reflective! 🤔",
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

class CustomPromptView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Set Custom Prompt", style=discord.ButtonStyle.primary, emoji="✏️")
    async def set_prompt(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="✏️ Set Custom Prompt",
            description="Use `!prompt set <your custom prompt>` to set a custom personality prompt for the bot.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Example",
            value="`!prompt set You are a helpful gaming buddy who loves Minecraft and always gives gaming tips`",
            inline=False
        )
        
        embed.add_field(
            name="Current Custom Prompt",
            value=self.bot.personality.get_custom_prompt(
                str(interaction.user.id), 
                str(interaction.guild.id) if interaction.guild else None
            ) or "None set (using default personality)",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Clear Prompt", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def clear_prompt(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.bot.personality.clear_custom_prompt(
            str(interaction.user.id),
            str(interaction.guild.id) if interaction.guild else None
        )
        
        embed = discord.Embed(
            title="✅ Custom Prompt Cleared",
            description="Your custom prompt has been cleared. The bot will now use the default personality modes.",
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

class FeatureView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Toggle Reactions", style=discord.ButtonStyle.primary)
    async def toggle_reactions(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_value = not self.bot.settings['reactions_enabled']
        self.bot.settings['reactions_enabled'] = new_value
        self.bot.config.set('reactions_enabled', new_value)
        status = "Enabled" if new_value else "Disabled"
        embed = discord.Embed(
            title="✅ Reactions Updated",
            description=f"Reactions {status}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Toggle Custom Prompts", style=discord.ButtonStyle.secondary)
    async def toggle_custom_prompts(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_value = not self.bot.settings['custom_prompt_enabled']
        self.bot.settings['custom_prompt_enabled'] = new_value
        self.bot.config.set('custom_prompt_enabled', new_value)
        status = "Enabled" if new_value else "Disabled"
        embed = discord.Embed(
            title="✅ Custom Prompts Updated",
            description=f"Custom prompts {status}",
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
        
    @commands.command(name="config", description="Configure bot settings")
    async def config(self, ctx):
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
            **Custom Prompts:** {'✅' if self.bot.settings['custom_prompt_enabled'] else '❌'}
            """,
            inline=False
        )
        
        view = ConfigView(self.bot)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))
