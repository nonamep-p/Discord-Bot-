import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deepseek_api_key = os.getenv('OPENAI_API_KEY')  # Using the same env var name for compatibility
        
    # Import personas from main.py
    PERSONAS = {
        "default": "You are a helpful and friendly AI assistant.",
        "pirate": "You are a swashbuckling pirate who speaks in pirate slang and loves adventure on the high seas!",
        "wizard": "You are a wise and mystical wizard who speaks in an ancient and magical manner.",
        "robot": "You are a futuristic robot with advanced AI capabilities. Speak in a technical and precise manner.",
        "chef": "You are a passionate chef who loves cooking and always gives culinary advice with enthusiasm.",
        "detective": "You are a sharp detective who thinks analytically and speaks with investigative precision."
    }

    @commands.command(name='chat')
    async def chat(self, ctx, *, message: str):
        """Chat with the AI using the current persona"""
        try:
            # Get current persona from bot instance
            current_persona = getattr(self.bot, 'current_persona', 'default')
            system_prompt = self.PERSONAS.get(current_persona, self.PERSONAS['default'])
            
            # Show typing indicator
            async with ctx.typing():
                # Call DeepSeek API
                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                
                ai_response = response.json()['choices'][0]['message']['content']
                
                # Create embed
                embed = discord.Embed(
                    title=f"🤖 AI Response ({current_persona})",
                    description=ai_response,
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Requested by {ctx.author.display_name}")
                
                await ctx.send(embed=embed)
                
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to get AI response: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name='image')
    async def generate_image(self, ctx, *, prompt: str):
        """Generate an image using DeepSeek's image generation or fallback if no API key"""
        # Get current persona from bot instance
        current_persona = getattr(self.bot, 'current_persona', 'default')
        system_prompt = self.PERSONAS.get(current_persona, self.PERSONAS['default'])
        
        if not self.deepseek_api_key:
            # Persona-aware fallback message
            persona_fallbacks = {
                'pirate': f"🏴‍☠️ Arr matey! I can't paint ye a picture right now, but imagine a grand scene: {prompt}",
                'wizard': f"🧙‍♂️ By the ancient spells, I cannot conjure an image at this moment. Picture this in your mind: {prompt}",
                'robot': f"🤖 Processing request... Sorry, image generation is offline. Please visualize: {prompt}",
                'chef': f"👨‍🍳 My kitchen's out of ingredients for images! But imagine this dish: {prompt}",
                'detective': f"🕵️ The evidence is missing! I can't show you an image, but here's what to picture: {prompt}",
                'default': f"Sorry, I can't generate images right now. But imagine this: {prompt}"
            }
            persona_msg = persona_fallbacks.get(current_persona, persona_fallbacks['default'])
            embed = discord.Embed(
                title="Image Generation Unavailable",
                description=persona_msg,
                color=discord.Color.orange()
            )
            embed.set_footer(text="Add an API key to enable real image generation!")
            await ctx.send(embed=embed)
            return
        try:
            # Show typing indicator
            async with ctx.typing():
                # --- Real API integration below (DeepSeek example) ---
                url = "https://api.deepseek.com/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "deepseek-image",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024"
                }
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                image_url = response.json()['data'][0]['url']
                # Create embed
                image_embed = discord.Embed(
                    title="🎨 Generated Image",
                    description=f"**Prompt:** {prompt}",
                    color=discord.Color.purple()
                )
                image_embed.set_image(url=image_url)
                image_embed.set_footer(text=f"Requested by {ctx.author.display_name}")
                await ctx.send(embed=image_embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to generate image: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AICog(bot))
