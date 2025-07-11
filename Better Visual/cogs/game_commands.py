
import discord
from discord.ext import commands
import random
import asyncio
import json
import time
from datetime import datetime, timedelta

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_questions = [
            {"question": "What's the largest planet in our solar system?", "answer": "jupiter", "options": ["Mars", "Jupiter", "Saturn", "Neptune"]},
            {"question": "Who painted the Mona Lisa?", "answer": "leonardo da vinci", "options": ["Picasso", "Van Gogh", "Leonardo da Vinci", "Michelangelo"]},
            {"question": "What's the capital of Japan?", "answer": "tokyo", "options": ["Osaka", "Tokyo", "Kyoto", "Hiroshima"]},
            {"question": "Which element has the chemical symbol 'O'?", "answer": "oxygen", "options": ["Gold", "Silver", "Oxygen", "Iron"]},
            {"question": "What year did World War II end?", "answer": "1945", "options": ["1944", "1945", "1946", "1947"]}
        ]
        
        self.active_games = {}
        self.user_stats = {}

    @commands.command(name='trivia')
    async def trivia(self, ctx):
        """Start a trivia question"""
        if ctx.channel.id in self.active_games:
            await ctx.send("There's already a game running in this channel! 🎮")
            return
            
        question_data = random.choice(self.trivia_questions)
        
        embed = discord.Embed(
            title="🧠 Trivia Time!",
            description=question_data["question"],
            color=discord.Color.blue()
        )
        
        options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(question_data["options"])])
        embed.add_field(name="Options:", value=options_text, inline=False)
        embed.set_footer(text="Type the number or answer! You have 30 seconds ⏰")
        
        self.active_games[ctx.channel.id] = {
            'type': 'trivia',
            'answer': question_data["answer"],
            'options': question_data["options"],
            'start_time': time.time()
        }
        
        await ctx.send(embed=embed)
        
        # Auto-end after 30 seconds
        await asyncio.sleep(30)
        if ctx.channel.id in self.active_games:
            del self.active_games[ctx.channel.id]
            await ctx.send(f"⏰ Time's up! The answer was: **{question_data['answer'].title()}**")

    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx, choice: str = None):
        """Play Rock Paper Scissors"""
        if not choice:
            embed = discord.Embed(
                title="✂️ Rock Paper Scissors",
                description="Choose: `!rps rock`, `!rps paper`, or `!rps scissors`",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            return
            
        choices = ['rock', 'paper', 'scissors']
        if choice.lower() not in choices:
            await ctx.send("Invalid choice! Use rock, paper, or scissors 🪨📄✂️")
            return
            
        bot_choice = random.choice(choices)
        user_choice = choice.lower()
        
        # Determine winner
        if user_choice == bot_choice:
            result = "It's a tie! 🤝"
            color = discord.Color.yellow()
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'paper' and bot_choice == 'rock') or \
             (user_choice == 'scissors' and bot_choice == 'paper'):
            result = "You win! 🎉"
            color = discord.Color.green()
        else:
            result = "I win! 😎"
            color = discord.Color.red()
            
        embed = discord.Embed(
            title="✂️ Rock Paper Scissors Result",
            description=f"You: {user_choice.title()}\nMe: {bot_choice.title()}\n\n**{result}**",
            color=color
        )
        await ctx.send(embed=embed)

    @commands.command(name='8ball')
    async def magic_8ball(self, ctx, *, question: str = None):
        """Ask the magic 8-ball a question"""
        if not question:
            await ctx.send("Ask me a question! Example: `!8ball Will it rain tomorrow?` 🎱")
            return
            
        responses = [
            "It is certain 🔮", "Reply hazy, try again 🌫️", "Don't count on it 🚫",
            "It is decidedly so ✅", "Ask again later ⏰", "My reply is no ❌",
            "Without a doubt 💯", "Better not tell you now 🤐", "My sources say no 📰",
            "Yes definitely 🎯", "Cannot predict now 🔄", "Outlook not so good 🌧️",
            "You may rely on it 🤝", "Concentrate and ask again 🧘", "Very doubtful 🤔",
            "As I see it, yes 👁️", "Most likely 📈", "Outlook good 🌞"
        ]
        
        response = random.choice(responses)
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {response}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name='guess')
    async def number_guess(self, ctx):
        """Start a number guessing game"""
        if ctx.channel.id in self.active_games:
            await ctx.send("There's already a game running! 🎮")
            return
            
        number = random.randint(1, 100)
        self.active_games[ctx.channel.id] = {
            'type': 'guess',
            'number': number,
            'attempts': 0,
            'start_time': time.time()
        }
        
        embed = discord.Embed(
            title="🔢 Number Guessing Game",
            description="I'm thinking of a number between 1 and 100!\nGuess by typing a number in chat 🎯",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle game responses"""
        if message.author.bot or message.channel.id not in self.active_games:
            return
            
        game = self.active_games[message.channel.id]
        
        if game['type'] == 'trivia':
            user_answer = message.content.lower().strip()
            correct_answer = game['answer'].lower()
            
            # Check if it's a number (option selection)
            if user_answer.isdigit():
                option_num = int(user_answer) - 1
                if 0 <= option_num < len(game['options']):
                    user_answer = game['options'][option_num].lower()
            
            if user_answer == correct_answer or any(correct_answer in user_answer for correct_answer in [correct_answer]):
                del self.active_games[message.channel.id]
                embed = discord.Embed(
                    title="🎉 Correct!",
                    description=f"Well done {message.author.mention}! The answer was **{game['answer'].title()}**",
                    color=discord.Color.green()
                )
                await message.channel.send(embed=embed)
                
        elif game['type'] == 'guess':
            try:
                guess = int(message.content)
                game['attempts'] += 1
                
                if guess == game['number']:
                    del self.active_games[message.channel.id]
                    embed = discord.Embed(
                        title="🎯 You got it!",
                        description=f"Congratulations {message.author.mention}! You guessed {game['number']} in {game['attempts']} attempts!",
                        color=discord.Color.gold()
                    )
                    await message.channel.send(embed=embed)
                elif guess < game['number']:
                    await message.add_reaction('⬆️')
                    await message.channel.send(f"Higher! 📈 (Attempt {game['attempts']})")
                else:
                    await message.add_reaction('⬇️')
                    await message.channel.send(f"Lower! 📉 (Attempt {game['attempts']})")
                    
            except ValueError:
                pass  # Not a number, ignore

async def setup(bot):
    await bot.add_cog(GamesCog(bot))
