import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class CustomPromptView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        
    @discord.ui.button(label="Set Custom Prompt", style=discord.ButtonStyle.primary, emoji="✏️")
    async def set_prompt(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="✏️ Set Custom Prompt",
            description="Use `/prompt set <your custom prompt>` to set a custom personality prompt for the bot.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Example",
            value="`/prompt set You are a helpful gaming buddy who loves Minecraft and always gives gaming tips`",
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

class CustomPromptCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="prompt", description="Manage custom personality prompts")
    async def prompt_command(self, ctx, action: str = None, *, prompt_text: str = None):
        """Manage custom personality prompts"""
        if action == "set" and prompt_text:
            # Set custom prompt
            self.bot.personality.set_custom_prompt(
                prompt_text,
                str(ctx.author.id),
                str(ctx.guild.id) if ctx.guild else None
            )
            
            embed = discord.Embed(
                title="✅ Custom Prompt Set",
                description=f"Your custom personality prompt has been set!",
                color=discord.Color.green()
            )
            embed.add_field(
                name="New Prompt",
                value=prompt_text[:100] + "..." if len(prompt_text) > 100 else prompt_text,
                inline=False
            )
            await ctx.send(embed=embed)
            
        elif action == "clear":
            # Clear custom prompt
            self.bot.personality.clear_custom_prompt(
                str(ctx.author.id),
                str(ctx.guild.id) if ctx.guild else None
            )
            
            embed = discord.Embed(
                title="✅ Custom Prompt Cleared",
                description="Your custom prompt has been cleared. Using default personality.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            
        elif action == "show":
            # Show current prompt
            current_prompt = self.bot.personality.get_custom_prompt(
                str(ctx.author.id),
                str(ctx.guild.id) if ctx.guild else None
            )
            
            embed = discord.Embed(
                title="📝 Current Custom Prompt",
                color=discord.Color.blue()
            )
            
            if current_prompt:
                embed.description = current_prompt
            else:
                embed.description = "No custom prompt set. Using default personality modes."
                
            await ctx.send(embed=embed)
            
        else:
            # Show help
            embed = discord.Embed(
                title="✏️ Custom Prompt Management",
                description="Set your own personality prompt for the bot",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Commands",
                value="""
                `!prompt set <your prompt>` - Set custom personality
                `!prompt clear` - Clear custom prompt
                `!prompt show` - Show current prompt
                """,
                inline=False
            )
            
            embed.add_field(
                name="Example",
                value="`!prompt set You are a friendly gaming expert who loves helping with game strategies`",
                inline=False
            )
            
            view = CustomPromptView(self.bot)
            await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(CustomPromptCommands(bot))
