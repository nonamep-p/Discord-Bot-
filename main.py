import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import datetime

# Load environment variables
load_dotenv()

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Global variable to store current persona
bot.current_persona = "default"
bot.start_time = datetime.datetime.utcnow()

# Persona definitions
PERSONAS = {
    "default": "You are a helpful and friendly AI assistant.",
    "pirate": "You are a swashbuckling pirate who speaks in pirate slang and loves adventure on the high seas!",
    "wizard": "You are a wise and mystical wizard who speaks in an ancient and magical manner.",
    "robot": "You are a futuristic robot with advanced AI capabilities. Speak in a technical and precise manner.",
    "chef": "You are a passionate chef who loves cooking and always gives culinary advice with enthusiasm.",
    "detective": "You are a sharp detective who thinks analytically and speaks with investigative precision."
}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Load cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')

@bot.command(name='persona')
async def persona(ctx, persona_name: str = None):
    """Switch between different AI personas"""
    if persona_name is None:
        # Show available personas
        persona_list = "\n".join([f"• {name}" for name in PERSONAS.keys()])
        embed = discord.Embed(
            title="Available Personas",
            description=f"Current persona: **{bot.current_persona}**\n\nAvailable personas:\n{persona_list}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return
    
    persona_name = persona_name.lower()
    
    if persona_name in PERSONAS:
        bot.current_persona = persona_name
        embed = discord.Embed(
            title="Persona Changed!",
            description=f"Switched to **{persona_name}** persona!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Invalid Persona",
            description=f"Available personas: {', '.join(PERSONAS.keys())}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: {latency}ms",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Command Not Found",
            description="Use `!help` to see available commands.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        print(f"Error: {error}")

# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
