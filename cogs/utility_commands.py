import discord
from discord.ext import commands
import datetime
import re
import asyncio
import random

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.todos = {}  # user_id: list of tasks

    @commands.command(name='bothelp')
    async def bothelp(self, ctx):
        """Show all available commands"""
        embed = discord.Embed(
            title="🤖 Discord AI Bot Commands",
            description="Here are all the available commands:",
            color=discord.Color.blue()
        )
        
        # AI Commands
        embed.add_field(
            name="🤖 AI Commands",
            value="""`!chat <message>` - Chat with AI using current persona
`!image <prompt>` - Generate image using DeepSeek
`!persona [name]` - Switch AI persona or list available personas""",
            inline=False
        )
        
        # Media Commands
        embed.add_field(
            name="🎬 Media Commands",
            value="""`!gif <search>` - Search for GIFs
`!meme` - Get a random meme""",
            inline=False
        )
        
        # Utility Commands
        embed.add_field(
            name="🔧 Utility Commands",
            value="""`!ping` - Check bot latency
`!serverinfo` - Get server information
`!userinfo [user]` - Get user information
`!bothelp` - Show this help message""",
            inline=False
        )
        
        embed.set_footer(text="Use !bothelp for detailed information about commands")
        await ctx.send(embed=embed)

    @commands.command(name='remindme')
    async def remindme(self, ctx, time: str, *, message: str):
        """Set a reminder: !remindme <time> <message> (e.g., !remindme 10m Take a break)"""
        seconds = self.parse_time(time)
        if seconds is None:
            await ctx.send("❌ Invalid time format! Use s/m/h/d (e.g., 10m, 2h, 1d)")
            return
        await ctx.send(f"⏰ Reminder set! I'll remind you in {time}.")
        await asyncio.sleep(seconds)
        try:
            await ctx.author.send(f"⏰ Reminder: {message}")
        except Exception:
            await ctx.send(f"⏰ {ctx.author.mention} Reminder: {message}")

    def parse_time(self, time_str):
        match = re.match(r"(\d+)([smhd])", time_str)
        if not match:
            return None
        value, unit = int(match.group(1)), match.group(2)
        if unit == 's': return value
        if unit == 'm': return value * 60
        if unit == 'h': return value * 3600
        if unit == 'd': return value * 86400
        return None

    @commands.group(name='todo', invoke_without_command=True)
    async def todo(self, ctx):
        """Show your to-do list"""
        user_id = str(ctx.author.id)
        tasks = self.todos.get(user_id, [])
        if not tasks:
            await ctx.send("📝 Your to-do list is empty!")
        else:
            msg = '\n'.join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
            await ctx.send(f"📝 **Your To-Do List:**\n{msg}")

    @todo.command(name='add')
    async def todo_add(self, ctx, *, task: str):
        """Add a task to your to-do list"""
        user_id = str(ctx.author.id)
        self.todos.setdefault(user_id, []).append(task)
        await ctx.send(f"✅ Task added: {task}")

    @todo.command(name='done')
    async def todo_done(self, ctx, task_number: int):
        """Mark a task as done and remove it from your to-do list"""
        user_id = str(ctx.author.id)
        tasks = self.todos.get(user_id, [])
        if 1 <= task_number <= len(tasks):
            removed = tasks.pop(task_number - 1)
            await ctx.send(f"✅ Task completed and removed: {removed}")
        else:
            await ctx.send("❌ Invalid task number!")

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        """Get information about the server"""
        guild = ctx.guild
        
        # Count channels by type
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        # Count members
        total_members = guild.member_count
        online_members = len([m for m in guild.members if m.status != discord.Status.offline])
        
        embed = discord.Embed(
            title=f"📊 {guild.name} Server Info",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="👑 Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="📅 Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
        
        embed.add_field(name="👥 Members", value=f"{online_members}/{total_members} online", inline=True)
        embed.add_field(name="📝 Text Channels", value=text_channels, inline=True)
        embed.add_field(name="🔊 Voice Channels", value=voice_channels, inline=True)
        
        embed.add_field(name="📂 Categories", value=categories, inline=True)
        embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        await ctx.send(embed=embed)

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get information about a user"""
        member = member or ctx.author
        
        # Get user roles (excluding @everyone)
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        roles.reverse()  # Show highest role first
        
        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color
        )
        
        embed.add_field(name="🆔 User ID", value=member.id, inline=True)
        embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="📅 Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        
        embed.add_field(name="🎭 Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name="🔰 Roles", value=" ".join(roles[:10]) if roles else "None", inline=False)
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
            
        await ctx.send(embed=embed)

    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Show bot uptime"""
        uptime = datetime.datetime.utcnow() - self.bot.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        embed = discord.Embed(
            title="⏰ Bot Uptime",
            description=f"🕐 {days}d {hours}h {minutes}m {seconds}s",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='8ball')
    async def eight_ball(self, ctx, *, question: str):
        """Ask the magic 8-ball a question"""
        persona = getattr(self.bot, 'current_persona', 'default')
        responses = {
            'default': [
                "It is certain.", "Without a doubt.", "You may rely on it.", "Yes, definitely.", "Most likely.",
                "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
                "Cannot predict now.", "Don't count on it.", "My reply is no.", "Very doubtful.", "Nope!"
            ],
            'pirate': [
                "Aye, it be true!", "Arrr, the seas say yes!", "Ye best try again, matey.", "Nay, not today.", "The winds be uncertain." 
            ],
            'wizard': [
                "By the ancient runes, yes.", "The stars align in your favor.", "The mists are unclear, try again.", "No, the fates say nay.", "Ask again under a full moon." 
            ],
            'robot': [
                "Affirmative.", "Negative.", "Insufficient data.", "Processing... try again.", "System error: ask later." 
            ]
        }
        msg = random.choice(responses.get(persona, responses['default']))
        await ctx.send(f"🎱 {msg}")

    @commands.group(name='quote', invoke_without_command=True)
    async def quote(self, ctx):
        """Show a random quote"""
        if not hasattr(self, 'quotes'):
            self.quotes = []
        if not self.quotes:
            await ctx.send("📜 No quotes saved yet! Use `!quote add <quote>` to add one.")
        else:
            await ctx.send(f"📜 {random.choice(self.quotes)}")

    @quote.command(name='add')
    async def quote_add(self, ctx, *, quote: str):
        """Add a quote to the list"""
        if not hasattr(self, 'quotes'):
            self.quotes = []
        self.quotes.append(f"{quote} — {ctx.author.display_name}")
        await ctx.send("✅ Quote added!")

    @quote.command(name='random')
    async def quote_random(self, ctx):
        """Show a random quote"""
        if not hasattr(self, 'quotes'):
            self.quotes = []
        if not self.quotes:
            await ctx.send("📜 No quotes saved yet!")
        else:
            await ctx.send(f"📜 {random.choice(self.quotes)}")

    @commands.command(name='roast')
    async def roast(self, ctx, member: discord.Member = None):
        """Send a friendly roast to a user"""
        member = member or ctx.author
        persona = getattr(self.bot, 'current_persona', 'default')
        roasts = {
            'default': [
                "You're as sharp as a marble!",
                "If I wanted to kill myself, I'd climb your ego and jump to your IQ.",
                "You have the right to remain silent because whatever you say will probably be stupid anyway.",
                "I'd agree with you but then we'd both be wrong.",
                "You're not stupid; you just have bad luck thinking."
            ],
            'pirate': [
                "Ye call that a comeback? I've seen parrots with better wit!",
                "Arrr, even the barnacles laugh at ye!",
                "Ye couldn't steal a laugh from a drunken sailor!"
            ],
            'wizard': [
                "By the beard of Merlin, your wit is as thin as a ghost!",
                "Even my old spellbook has more charm than you.",
                "You must have been hit with a confusion hex at birth!"
            ],
            'robot': [
                "01010011 01100001 01110110 01100001 01100111 01100101 00100000 01100101 01110010 01110010 01101111 01110010.",
                "Your logic circuits are malfunctioning.",
                "Error 404: Comeback not found."
            ]
        }
        msg = random.choice(roasts.get(persona, roasts['default']))
        await ctx.send(f"🔥 {member.mention} {msg}")

    @commands.command(name='poll')
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, question_and_options: str):
        """Create a poll: !poll <question> | <option1> | <option2> ..."""
        parts = [p.strip() for p in question_and_options.split('|')]
        if len(parts) < 3:
            await ctx.send("❌ Usage: !poll <question> | <option1> | <option2> ... (at least 2 options)")
            return
        question, options = parts[0], parts[1:]
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        if len(options) > len(emojis):
            await ctx.send(f"❌ Max {len(emojis)} options allowed.")
            return
        desc = '\n'.join(f"{emojis[i]} {opt}" for i, opt in enumerate(options))
        embed = discord.Embed(title=f"📊 {question}", description=desc, color=discord.Color.blue())
        poll_msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_msg.add_reaction(emojis[i])

    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Set slowmode for the current channel: !slowmode <seconds> (0 to disable)"""
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send("🐢 Slowmode disabled!")
        else:
            await ctx.send(f"🐢 Slowmode set to {seconds} seconds.")

    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):
        """Bulk delete messages: !purge <number> (max 100)"""
        if count < 1 or count > 100:
            await ctx.send("❌ Can only purge 1-100 messages at a time.")
            return
        deleted = await ctx.channel.purge(limit=count+1)  # +1 to include the command
        await ctx.send(f"🧹 Deleted {len(deleted)-1} messages.", delete_after=3)

    # --- Welcome/Goodbye Messages ---
    @commands.group(name='welcome', invoke_without_command=True)
    async def welcome(self, ctx):
        """Show current welcome/goodbye messages"""
        guild_id = str(ctx.guild.id)
        welcome = getattr(self.bot, 'welcome_messages', {})
        msg = welcome.get(guild_id, {'welcome': None, 'goodbye': None})
        await ctx.send(f"👋 Welcome: {msg['welcome'] or 'Not set'}\n👋 Goodbye: {msg['goodbye'] or 'Not set'}")

    @welcome.command(name='set')
    async def welcome_set(self, ctx, type: str, *, message: str):
        """Set welcome or goodbye message: !welcome set <welcome/goodbye> <message>"""
        guild_id = str(ctx.guild.id)
        if not hasattr(self.bot, 'welcome_messages'):
            self.bot.welcome_messages = {}
        if guild_id not in self.bot.welcome_messages:
            self.bot.welcome_messages[guild_id] = {'welcome': None, 'goodbye': None}
        if type not in ['welcome', 'goodbye']:
            await ctx.send("❌ Type must be 'welcome' or 'goodbye'.")
            return
        self.bot.welcome_messages[guild_id][type] = message
        await ctx.send(f"✅ {type.title()} message set!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        welcome = getattr(self.bot, 'welcome_messages', {})
        msg = welcome.get(guild_id, {}).get('welcome')
        if msg:
            try:
                await member.send(msg)
            except Exception:
                channel = member.guild.system_channel or next((c for c in member.guild.text_channels if c.permissions_for(member.guild.me).send_messages), None)
                if channel:
                    await channel.send(f"👋 {member.mention} {msg}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = str(member.guild.id)
        welcome = getattr(self.bot, 'welcome_messages', {})
        msg = welcome.get(guild_id, {}).get('goodbye')
        if msg:
            channel = member.guild.system_channel or next((c for c in member.guild.text_channels if c.permissions_for(member.guild.me).send_messages), None)
            if channel:
                await channel.send(f"👋 {member.display_name} {msg}")

    # --- Banned Words Filter ---
    @commands.group(name='bannedwords', invoke_without_command=True)
    async def bannedwords(self, ctx):
        """Show banned words list"""
        guild_id = str(ctx.guild.id)
        banned = getattr(self.bot, 'banned_words', {})
        words = banned.get(guild_id, set())
        await ctx.send(f"🚫 Banned words: {', '.join(words) if words else 'None'}")

    @bannedwords.command(name='add')
    async def bannedwords_add(self, ctx, *, word: str):
        guild_id = str(ctx.guild.id)
        if not hasattr(self.bot, 'banned_words'):
            self.bot.banned_words = {}
        self.bot.banned_words.setdefault(guild_id, set()).add(word.lower())
        await ctx.send(f"✅ Banned word added: {word}")

    @bannedwords.command(name='remove')
    async def bannedwords_remove(self, ctx, *, word: str):
        guild_id = str(ctx.guild.id)
        if hasattr(self.bot, 'banned_words') and word.lower() in self.bot.banned_words.get(guild_id, set()):
            self.bot.banned_words[guild_id].remove(word.lower())
            await ctx.send(f"✅ Banned word removed: {word}")
        else:
            await ctx.send("❌ Word not found in banned list.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        guild_id = str(message.guild.id) if message.guild else None
        banned = getattr(self.bot, 'banned_words', {})
        words = banned.get(guild_id, set())
        if words and any(word in message.content.lower() for word in words):
            try:
                await message.delete()
                await message.channel.send(f"🚫 Message deleted: banned word used.", delete_after=3)
            except Exception:
                pass
        await self.bot.process_commands(message)

    # --- User Profile, Avatar, Stats, Invite ---
    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"🧑 Profile: {member.display_name}", color=member.color)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined", value=member.joined_at.strftime('%Y-%m-%d'))
        embed.add_field(name="Account Created", value=member.created_at.strftime('%Y-%m-%d'))
        embed.add_field(name="Roles", value=", ".join([r.name for r in member.roles if r.name != '@everyone']) or 'None')
        embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)

    @commands.command(name='avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        if member.avatar:
            embed = discord.Embed(title=f"🖼️ {member.display_name}'s Avatar", color=member.color)
            embed.set_image(url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ No avatar found.")

    @commands.command(name='stats')
    async def stats(self, ctx):
        embed = discord.Embed(title="📊 Bot Stats", color=discord.Color.green())
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(set(self.bot.get_all_members())))
        embed.add_field(name="Ping", value=f"{round(self.bot.latency*1000)}ms")
        await ctx.send(embed=embed)

    @commands.command(name='invite')
    async def invite(self, ctx):
        client_id = (self.bot.user.id if self.bot.user else 'YOUR_CLIENT_ID')
        url = f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot%20applications.commands"
        await ctx.send(f"🔗 [Invite me to your server!]({url})")

    # --- Mini-Games: RPS, Guess ---
    @commands.command(name='rps')
    async def rps(self, ctx, choice: str):
        """Play rock-paper-scissors: !rps <rock|paper|scissors>"""
        options = ['rock', 'paper', 'scissors']
        if choice.lower() not in options:
            await ctx.send("❌ Choose rock, paper, or scissors.")
            return
        bot_choice = random.choice(options)
        result = self.rps_result(choice.lower(), bot_choice)
        await ctx.send(f"🪨📄✂️ You: {choice.capitalize()} | Bot: {bot_choice.capitalize()}\n**{result}**")

    def rps_result(self, user, bot):
        if user == bot:
            return "It's a tie!"
        wins = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
        if wins[user] == bot:
            return "You win!"
        return "I win!"

    @commands.command(name='guess')
    async def guess(self, ctx, number: int):
        """Guess a number between 1 and 10"""
        answer = random.randint(1, 10)
        if number == answer:
            await ctx.send(f"🎉 Correct! The number was {answer}.")
        else:
            await ctx.send(f"❌ Nope! The number was {answer}.")

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
