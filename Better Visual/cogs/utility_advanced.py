
import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import json
import re
from typing import Dict, List

class AdvancedUtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}
        self.reaction_roles = {}
        self.auto_responses = {}
        self.check_reminders.start()

    @commands.command(name='remind')
    async def remind(self, ctx, time_str: str = None, *, reminder_text: str = None):
        """Set a reminder - Examples: !remind 5m Take a break, !remind 1h Meeting"""
        if not time_str or not reminder_text:
            await ctx.send("❌ Usage: `!remind <time> <reminder>`\nExamples: `!remind 5m Take a break` or `!remind 2h Meeting`")
            return
            
        # Parse time
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        match = re.match(r'(\d+)([smhd])', time_str.lower())
        
        if not match:
            await ctx.send("❌ Invalid time format! Use: 5s, 10m, 2h, or 1d")
            return
            
        amount, unit = match.groups()
        seconds = int(amount) * time_units[unit]
        
        if seconds > 86400 * 7:  # Max 7 days
            await ctx.send("❌ Maximum reminder time is 7 days!")
            return
            
        remind_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        
        reminder_id = f"{ctx.author.id}_{len(self.reminders)}"
        self.reminders[reminder_id] = {
            'user_id': ctx.author.id,
            'channel_id': ctx.channel.id,
            'reminder': reminder_text,
            'time': remind_time,
            'created': datetime.datetime.now()
        }
        
        embed = discord.Embed(
            title="⏰ Reminder Set!",
            description=f"I'll remind you about: **{reminder_text}**",
            color=discord.Color.green()
        )
        embed.add_field(name="When", value=f"In {amount}{unit} ({remind_time.strftime('%Y-%m-%d %H:%M')})", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='translate')
    async def translate_text(self, ctx, language: str = None, *, text: str = None):
        """Translate text to different languages"""
        if not language or not text:
            await ctx.send("❌ Usage: `!translate <language> <text>`\nExample: `!translate spanish Hello world`")
            return
            
        # Simple translation dictionary (expand as needed)
        translations = {
            'spanish': {'hello': 'hola', 'world': 'mundo', 'good': 'bueno', 'bye': 'adiós'},
            'french': {'hello': 'bonjour', 'world': 'monde', 'good': 'bon', 'bye': 'au revoir'},
            'german': {'hello': 'hallo', 'world': 'welt', 'good': 'gut', 'bye': 'tschüss'},
            'italian': {'hello': 'ciao', 'world': 'mondo', 'good': 'buono', 'bye': 'ciao'}
        }
        
        language = language.lower()
        if language not in translations:
            available = ', '.join(translations.keys())
            await ctx.send(f"❌ Language not supported! Available: {available}")
            return
            
        # Basic word-by-word translation
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            if word in translations[language]:
                translated_words.append(translations[language][word])
            else:
                translated_words.append(word)  # Keep original if not found
                
        translated_text = ' '.join(translated_words)
        
        embed = discord.Embed(
            title="🌍 Translation",
            color=discord.Color.blue()
        )
        embed.add_field(name="Original", value=text, inline=False)
        embed.add_field(name=f"Translated ({language.title()})", value=translated_text, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='reactionrole')
    @commands.has_permissions(manage_roles=True)
    async def reaction_role(self, ctx, message_id: int = None, emoji: str = None, role: discord.Role = None):
        """Set up reaction roles"""
        if not message_id or not emoji or not role:
            await ctx.send("❌ Usage: `!reactionrole <message_id> <emoji> <role>`")
            return
            
        try:
            message = await ctx.channel.fetch_message(message_id)
            await message.add_reaction(emoji)
            
            self.reaction_roles[message_id] = {
                'emoji': emoji,
                'role_id': role.id,
                'guild_id': ctx.guild.id
            }
            
            embed = discord.Embed(
                title="✅ Reaction Role Set!",
                description=f"React with {emoji} to get {role.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            await ctx.send("❌ Message not found!")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='autoresponse')
    @commands.has_permissions(manage_guild=True)
    async def auto_response(self, ctx, trigger: str = None, *, response: str = None):
        """Set up automatic responses to specific words"""
        if not trigger or not response:
            await ctx.send("❌ Usage: `!autoresponse <trigger> <response>`\nExample: `!autoresponse hello Hey there!`")
            return
            
        guild_id = str(ctx.guild.id)
        if guild_id not in self.auto_responses:
            self.auto_responses[guild_id] = {}
            
        self.auto_responses[guild_id][trigger.lower()] = response
        
        embed = discord.Embed(
            title="✅ Auto Response Set!",
            description=f"Bot will respond with: **{response}**\nWhen someone says: **{trigger}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='weather')
    async def weather(self, ctx, *, location: str = None):
        """Get weather information (mock data)"""
        if not location:
            await ctx.send("❌ Please specify a location!\nExample: `!weather New York`")
            return
            
        # Mock weather data (in real implementation, use weather API)
        weather_conditions = ['Sunny', 'Cloudy', 'Rainy', 'Snowy', 'Partly Cloudy']
        temperature = random.randint(-10, 35)
        condition = random.choice(weather_conditions)
        humidity = random.randint(30, 90)
        
        weather_emojis = {
            'Sunny': '☀️',
            'Cloudy': '☁️', 
            'Rainy': '🌧️',
            'Snowy': '❄️',
            'Partly Cloudy': '⛅'
        }
        
        embed = discord.Embed(
            title=f"🌤️ Weather in {location.title()}",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Condition", value=f"{weather_emojis[condition]} {condition}", inline=True)
        embed.add_field(name="Temperature", value=f"🌡️ {temperature}°C", inline=True)
        embed.add_field(name="Humidity", value=f"💧 {humidity}%", inline=True)
        
        await ctx.send(embed=embed)

    @tasks.loop(seconds=30)
    async def check_reminders(self):
        """Check for due reminders"""
        current_time = datetime.datetime.now()
        due_reminders = []
        
        for reminder_id, reminder_data in self.reminders.items():
            if current_time >= reminder_data['time']:
                due_reminders.append(reminder_id)
                
        for reminder_id in due_reminders:
            reminder = self.reminders[reminder_id]
            
            try:
                user = self.bot.get_user(reminder['user_id'])
                channel = self.bot.get_channel(reminder['channel_id'])
                
                if user and channel:
                    embed = discord.Embed(
                        title="⏰ Reminder!",
                        description=reminder['reminder'],
                        color=discord.Color.orange()
                    )
                    embed.set_footer(text=f"Set {reminder['created'].strftime('%Y-%m-%d %H:%M')}")
                    await channel.send(f"{user.mention}", embed=embed)
                    
            except Exception as e:
                print(f"Error sending reminder: {e}")
                
            del self.reminders[reminder_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle auto responses"""
        if message.author.bot:
            return
            
        guild_id = str(message.guild.id) if message.guild else None
        if guild_id in self.auto_responses:
            content = message.content.lower()
            
            for trigger, response in self.auto_responses[guild_id].items():
                if trigger in content:
                    await message.channel.send(response)
                    break

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle reaction roles"""
        if user.bot:
            return
            
        message_id = reaction.message.id
        if message_id in self.reaction_roles:
            role_data = self.reaction_roles[message_id]
            
            if str(reaction.emoji) == role_data['emoji']:
                guild = self.bot.get_guild(role_data['guild_id'])
                role = guild.get_role(role_data['role_id'])
                member = guild.get_member(user.id)
                
                if role and member and role not in member.roles:
                    try:
                        await member.add_roles(role)
                    except Exception as e:
                        print(f"Error adding role: {e}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        """Handle reaction role removal"""
        if user.bot:
            return
            
        message_id = reaction.message.id
        if message_id in self.reaction_roles:
            role_data = self.reaction_roles[message_id]
            
            if str(reaction.emoji) == role_data['emoji']:
                guild = self.bot.get_guild(role_data['guild_id'])
                role = guild.get_role(role_data['role_id'])
                member = guild.get_member(user.id)
                
                if role and member and role in member.roles:
                    try:
                        await member.remove_roles(role)
                    except Exception as e:
                        print(f"Error removing role: {e}")

async def setup(bot):
    await bot.add_cog(AdvancedUtilityCog(bot))
