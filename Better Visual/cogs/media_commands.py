import discord
from discord.ext import commands
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

class MediaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giphy_api_key = os.getenv('GIPHY_API_KEY')

    @commands.command(name='gif')
    async def gif(self, ctx, *, query: str):
        """Search for a GIF using Giphy"""
        try:
            if not self.giphy_api_key:
                embed = discord.Embed(
                    title="❌ Error",
                    description="Giphy API key not configured. Please add GIPHY_API_KEY to your .env file.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            # Show typing indicator
            async with ctx.typing():
                # Giphy search API
                url = "https://api.giphy.com/v1/gifs/search"
                params = {
                    'api_key': self.giphy_api_key,
                    'q': query,
                    'limit': 25,
                    'rating': 'g'
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                if data['data']:
                    # Pick a random GIF from results
                    gif = random.choice(data['data'])
                    gif_url = gif['images']['original']['url']
                    
                    # Create embed
                    embed = discord.Embed(
                        title="🎬 GIF Found!",
                        description=f"**Search:** {query}",
                        color=discord.Color.green()
                    )
                    embed.set_image(url=gif_url)
                    embed.set_footer(text=f"Requested by {ctx.author.display_name}")
                    
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ No GIFs Found",
                        description=f"No GIFs found for: {query}",
                        color=discord.Color.orange()
                    )
                    await ctx.send(embed=embed)
                    
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to fetch GIF: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name='meme')
    async def meme(self, ctx):
        """Get a random meme from Reddit"""
        try:
            # Show typing indicator
            async with ctx.typing():
                # Reddit API (no auth required for public endpoints)
                url = "https://www.reddit.com/r/memes/random.json"
                headers = {'User-Agent': 'DiscordBot/1.0'}
                
                response = requests.get(url, headers=headers)
                data = response.json()
                
                if 'data' in data and 'children' in data['data']:
                    post = data['data']['children'][0]['data']
                    title = post['title']
                    image_url = post['url']
                    
                    # Only proceed if it's an image
                    if any(ext in image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                        embed = discord.Embed(
                            title="😂 Random Meme",
                            description=title,
                            color=discord.Color.orange()
                        )
                        embed.set_image(url=image_url)
                        embed.set_footer(text=f"From r/memes | Requested by {ctx.author.display_name}")
                        
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="❌ Error",
                            description="The random post wasn't an image. Try again!",
                            color=discord.Color.red()
                        )
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Error",
                        description="Failed to fetch meme from Reddit",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
                    
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Failed to fetch meme: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MediaCog(bot))
