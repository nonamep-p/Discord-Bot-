
import discord
from discord.ext import commands
import random
import asyncio
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.trivia_questions = [
            {"question": "What is the capital of France?", "answer": "paris", "options": ["London", "Berlin", "Paris", "Madrid"]},
            {"question": "Which planet is known as the Red Planet?", "answer": "mars", "options": ["Venus", "Mars", "Jupiter", "Saturn"]},
            {"question": "What is 2 + 2?", "answer": "4", "options": ["3", "4", "5", "6"]},
            {"question": "Who wrote Romeo and Juliet?", "answer": "shakespeare", "options": ["Dickens", "Shakespeare", "Austen", "Orwell"]},
            {"question": "What is the largest mammal?", "answer": "blue whale", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippo"]},
        ]
        
    @commands.command(name='trivia')
    async def trivia(self, ctx):
        """Play trivia for coins"""
        user_id = str(ctx.author.id)
        
        if user_id in self.active_games:
            await ctx.send("❌ You already have an active game!")
            return
            
        question = random.choice(self.trivia_questions)
        self.active_games[user_id] = {
            'type': 'trivia',
            'question': question,
            'start_time': datetime.now()
        }
        
        embed = discord.Embed(
            title="🧠 Trivia Question",
            description=question['question'],
            color=discord.Color.blue()
        )
        
        for i, option in enumerate(question['options'], 1):
            embed.add_field(name=f"{i}.", value=option, inline=True)
            
        embed.set_footer(text="Type the number or answer to respond! (30 seconds)")
        
        await ctx.send(embed=embed)
        
        try:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
                
            response = await self.bot.wait_for('message', check=check, timeout=30)
            
            # Check answer
            user_answer = response.content.lower().strip()
            correct_answer = question['answer'].lower()
            
            is_correct = False
            if user_answer in correct_answer or correct_answer in user_answer:
                is_correct = True
            elif user_answer.isdigit():
                option_index = int(user_answer) - 1
                if 0 <= option_index < len(question['options']):
                    if question['options'][option_index].lower() == correct_answer:
                        is_correct = True
                        
            if is_correct:
                reward = random.randint(50, 150)
                self.bot.db.add_coins(user_id, reward)
                
                embed = discord.Embed(
                    title="🎉 Correct!",
                    description=f"You earned **{reward} coins**!",
                    color=discord.Color.green()
                )
                
                # Achievement check
                self.check_trivia_achievement(user_id)
            else:
                embed = discord.Embed(
                    title="❌ Incorrect!",
                    description=f"The correct answer was: **{question['answer']}**",
                    color=discord.Color.red()
                )
                
            del self.active_games[user_id]
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            del self.active_games[user_id]
            await ctx.send("⏰ Time's up! The game has ended.")
            
    @commands.command(name='wordle')
    async def wordle(self, ctx):
        """Play Wordle game"""
        user_id = str(ctx.author.id)
        
        if user_id in self.active_games:
            await ctx.send("❌ You already have an active game!")
            return
            
        words = ['PLANE', 'HOUSE', 'WORLD', 'PEACE', 'DANCE', 'MUSIC', 'LIGHT', 'HEART', 'SMILE', 'BRAVE']
        target_word = random.choice(words)
        
        self.active_games[user_id] = {
            'type': 'wordle',
            'word': target_word,
            'guesses': [],
            'max_guesses': 6
        }
        
        embed = discord.Embed(
            title="🔤 Wordle Game",
            description="Guess the 5-letter word!\n\n🟩 = Correct letter in correct position\n🟨 = Correct letter in wrong position\n⬜ = Letter not in word",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Instructions", value="Type your 5-letter guess!", inline=False)
        embed.add_field(name="Guesses Left", value="6", inline=True)
        
        await ctx.send(embed=embed)
        
        game_data = self.active_games[user_id]
        
        while len(game_data['guesses']) < game_data['max_guesses']:
            try:
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel and len(m.content) == 5
                    
                response = await self.bot.wait_for('message', check=check, timeout=60)
                guess = response.content.upper()
                
                if not guess.isalpha():
                    await ctx.send("❌ Please enter only letters!")
                    continue
                    
                game_data['guesses'].append(guess)
                
                # Generate feedback
                feedback = ""
                for i, letter in enumerate(guess):
                    if letter == target_word[i]:
                        feedback += "🟩"
                    elif letter in target_word:
                        feedback += "🟨"
                    else:
                        feedback += "⬜"
                        
                embed = discord.Embed(
                    title="🔤 Wordle Game",
                    color=discord.Color.green()
                )
                
                # Show all guesses
                guess_display = ""
                for i, g in enumerate(game_data['guesses']):
                    g_feedback = ""
                    for j, letter in enumerate(g):
                        if letter == target_word[j]:
                            g_feedback += "🟩"
                        elif letter in target_word:
                            g_feedback += "🟨"
                        else:
                            g_feedback += "⬜"
                    guess_display += f"{g} {g_feedback}\n"
                    
                embed.add_field(name="Your Guesses", value=guess_display, inline=False)
                
                if guess == target_word:
                    reward = (7 - len(game_data['guesses'])) * 25  # More reward for fewer guesses
                    self.bot.db.add_coins(user_id, reward)
                    
                    embed.add_field(
                        name="🎉 You Won!",
                        value=f"Correct! The word was **{target_word}**\nYou earned **{reward} coins**!",
                        inline=False
                    )
                    
                    del self.active_games[user_id]
                    await ctx.send(embed=embed)
                    return
                    
                guesses_left = game_data['max_guesses'] - len(game_data['guesses'])
                embed.add_field(name="Guesses Left", value=str(guesses_left), inline=True)
                
                await ctx.send(embed=embed)
                
            except asyncio.TimeoutError:
                await ctx.send("⏰ Game timed out!")
                del self.active_games[user_id]
                return
                
        # Game over - no more guesses
        embed = discord.Embed(
            title="💔 Game Over",
            description=f"You ran out of guesses! The word was **{target_word}**",
            color=discord.Color.red()
        )
        
        del self.active_games[user_id]
        await ctx.send(embed=embed)
        
    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx, choice: str = None):
        """Play Rock Paper Scissors"""
        if not choice:
            embed = discord.Embed(
                title="✂️ Rock Paper Scissors",
                description="Choose: `rock`, `paper`, or `scissors`",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
            
        user_choice = choice.lower()
        if user_choice not in ['rock', 'paper', 'scissors']:
            await ctx.send("❌ Invalid choice! Use `rock`, `paper`, or `scissors`")
            return
            
        bot_choice = random.choice(['rock', 'paper', 'scissors'])
        
        emojis = {'rock': '🗿', 'paper': '📄', 'scissors': '✂️'}
        
        embed = discord.Embed(title="✂️ Rock Paper Scissors", color=discord.Color.blue())
        embed.add_field(name="Your Choice", value=f"{emojis[user_choice]} {user_choice.title()}", inline=True)
        embed.add_field(name="Bot's Choice", value=f"{emojis[bot_choice]} {bot_choice.title()}", inline=True)
        
        user_id = str(ctx.author.id)
        
        if user_choice == bot_choice:
            embed.add_field(name="Result", value="🤝 It's a tie!", inline=False)
            embed.color = discord.Color.orange()
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'paper' and bot_choice == 'rock') or \
             (user_choice == 'scissors' and bot_choice == 'paper'):
            reward = random.randint(20, 50)
            self.bot.db.add_coins(user_id, reward)
            embed.add_field(name="Result", value=f"🎉 You win! +{reward} coins", inline=False)
            embed.color = discord.Color.green()
        else:
            embed.add_field(name="Result", value="😞 You lose!", inline=False)
            embed.color = discord.Color.red()
            
        await ctx.send(embed=embed)
        
    @commands.command(name='guess')
    async def number_guess(self, ctx, number: int = None):
        """Guess a number between 1-10"""
        if number is None:
            await ctx.send("Usage: `!guess <number>` (1-10)")
            return
            
        if not 1 <= number <= 10:
            await ctx.send("❌ Number must be between 1 and 10!")
            return
            
        bot_number = random.randint(1, 10)
        user_id = str(ctx.author.id)
        
        embed = discord.Embed(title="🎲 Number Guessing Game", color=discord.Color.blue())
        embed.add_field(name="Your Guess", value=str(number), inline=True)
        embed.add_field(name="My Number", value=str(bot_number), inline=True)
        
        if number == bot_number:
            reward = random.randint(100, 200)
            self.bot.db.add_coins(user_id, reward)
            embed.add_field(name="Result", value=f"🎉 Correct! You won {reward} coins!", inline=False)
            embed.color = discord.Color.green()
        else:
            embed.add_field(name="Result", value="😞 Wrong number! Better luck next time!", inline=False)
            embed.color = discord.Color.red()
            
        await ctx.send(embed=embed)
        
    @commands.command(name='mathchallenge')
    async def math_challenge(self, ctx):
        """Solve math problems for coins"""
        user_id = str(ctx.author.id)
        
        if user_id in self.active_games:
            await ctx.send("❌ You already have an active game!")
            return
            
        # Generate random math problem
        operations = ['+', '-', '*']
        operation = random.choice(operations)
        
        if operation == '+':
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
            answer = num1 + num2
        elif operation == '-':
            num1 = random.randint(50, 99)
            num2 = random.randint(10, num1)
            answer = num1 - num2
        else:  # multiplication
            num1 = random.randint(5, 15)
            num2 = random.randint(5, 15)
            answer = num1 * num2
            
        problem = f"{num1} {operation} {num2}"
        
        self.active_games[user_id] = {
            'type': 'math',
            'answer': answer,
            'start_time': datetime.now()
        }
        
        embed = discord.Embed(
            title="🧮 Math Challenge",
            description=f"**{problem} = ?**",
            color=discord.Color.blue()
        )
        
        embed.set_footer(text="Type your answer! (15 seconds)")
        
        await ctx.send(embed=embed)
        
        try:
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
                
            response = await self.bot.wait_for('message', check=check, timeout=15)
            
            try:
                user_answer = int(response.content)
                
                if user_answer == answer:
                    # Calculate reward based on speed
                    time_taken = (datetime.now() - self.active_games[user_id]['start_time']).total_seconds()
                    base_reward = 30
                    speed_bonus = max(0, int((15 - time_taken) * 5))
                    total_reward = base_reward + speed_bonus
                    
                    self.bot.db.add_coins(user_id, total_reward)
                    
                    embed = discord.Embed(
                        title="🎉 Correct!",
                        description=f"**{problem} = {answer}**\nYou earned **{total_reward} coins**!",
                        color=discord.Color.green()
                    )
                    
                    if speed_bonus > 0:
                        embed.add_field(name="⚡ Speed Bonus", value=f"+{speed_bonus} coins", inline=True)
                        
                else:
                    embed = discord.Embed(
                        title="❌ Incorrect!",
                        description=f"**{problem} = {answer}**",
                        color=discord.Color.red()
                    )
                    
            except ValueError:
                embed = discord.Embed(
                    title="❌ Invalid Answer!",
                    description=f"**{problem} = {answer}**",
                    color=discord.Color.red()
                )
                
            del self.active_games[user_id]
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            del self.active_games[user_id]
            embed = discord.Embed(
                title="⏰ Time's Up!",
                description=f"**{problem} = {answer}**",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            
    @commands.command(name='wordgame')
    async def word_game(self, ctx):
        """Word association game"""
        user_id = str(ctx.author.id)
        
        if user_id in self.active_games:
            await ctx.send("❌ You already have an active game!")
            return
            
        word_chains = {
            'animal': ['dog', 'cat', 'bird', 'fish', 'lion', 'tiger', 'elephant'],
            'food': ['pizza', 'burger', 'salad', 'soup', 'bread', 'cheese', 'fruit'],
            'color': ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink'],
            'sport': ['football', 'basketball', 'tennis', 'swimming', 'running', 'cycling']
        }
        
        category = random.choice(list(word_chains.keys()))
        target_words = word_chains[category]
        
        self.active_games[user_id] = {
            'type': 'word',
            'category': category,
            'target_words': target_words,
            'found_words': [],
            'start_time': datetime.now()
        }
        
        embed = discord.Embed(
            title="📝 Word Association Game",
            description=f"Name words related to: **{category.upper()}**\n\nType one word at a time! (60 seconds)",
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=embed)
        
        game_data = self.active_games[user_id]
        end_time = datetime.now() + timedelta(seconds=60)
        
        while datetime.now() < end_time:
            try:
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                    
                response = await self.bot.wait_for('message', check=check, timeout=10)
                word = response.content.lower().strip()
                
                if word in target_words and word not in game_data['found_words']:
                    game_data['found_words'].append(word)
                    await response.add_reaction('✅')
                    
                    if len(game_data['found_words']) >= len(target_words):
                        break
                        
            except asyncio.TimeoutError:
                break
                
        # Game finished
        score = len(game_data['found_words'])
        total_possible = len(target_words)
        reward = score * 25
        
        if reward > 0:
            self.bot.db.add_coins(user_id, reward)
            
        embed = discord.Embed(
            title="📝 Word Game Complete!",
            description=f"Category: **{category.upper()}**\nYou found **{score}/{total_possible}** words!",
            color=discord.Color.green() if score > 0 else discord.Color.orange()
        )
        
        if game_data['found_words']:
            embed.add_field(name="Words Found", value=", ".join(game_data['found_words']), inline=False)
            
        if reward > 0:
            embed.add_field(name="💰 Reward", value=f"{reward} coins", inline=True)
            
        del self.active_games[user_id]
        await ctx.send(embed=embed)
        
    def check_trivia_achievement(self, user_id):
        """Check and award trivia achievements"""
        user_data = self.bot.db.get_user(user_id)
        trivia_wins = user_data.get('trivia_wins', 0) + 1
        
        self.bot.db.update_user_data(user_id, {'trivia_wins': trivia_wins})
        
        # Award achievements
        if trivia_wins == 10:
            self.bot.db.add_coins(user_id, 500)
            # Could send achievement notification here
            
    @commands.command(name='games')
    async def games_menu(self, ctx):
        """Show all available games"""
        embed = discord.Embed(
            title="🎮 Game Center",
            description="Play games to earn coins and have fun!",
            color=discord.Color.gold()
        )
        
        embed.add_field(
            name="🧠 Trivia",
            value="`!trivia` - Answer questions for coins",
            inline=True
        )
        
        embed.add_field(
            name="🔤 Wordle",
            value="`!wordle` - Guess the 5-letter word",
            inline=True
        )
        
        embed.add_field(
            name="✂️ Rock Paper Scissors",
            value="`!rps <choice>` - Classic game",
            inline=True
        )
        
        embed.add_field(
            name="🎲 Number Guess",
            value="`!guess <1-10>` - Guess my number",
            inline=True
        )
        
        embed.add_field(
            name="🧮 Math Challenge",
            value="`!mathchallenge` - Solve math problems",
            inline=True
        )
        
        embed.add_field(
            name="📝 Word Game",
            value="`!wordgame` - Word association",
            inline=True
        )
        
        embed.add_field(
            name="🎰 Gambling Games",
            value="`!slots <amount>` - Slot machine\n`!blackjack <amount>` - Card game",
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GamesCog(bot))
import discord
from discord.ext import commands
import random
import asyncio
import logging

logger = logging.getLogger(__name__)

class GameCommands(commands.Cog):
    """Fun mini-games and entertainment commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}  # Track active games
        
    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx, choice: str = None):
        """Play rock paper scissors"""
        if not choice:
            await ctx.send("🎮 Usage: `!rps <rock/paper/scissors>`")
            return
        
        choices = ['rock', 'paper', 'scissors']
        user_choice = choice.lower()
        
        if user_choice not in choices:
            await ctx.send("❌ Invalid choice! Choose rock, paper, or scissors.")
            return
        
        bot_choice = random.choice(choices)
        
        # Determine winner
        if user_choice == bot_choice:
            result = "It's a tie!"
            color = 0xFFFF00
            reward = 10
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'paper' and bot_choice == 'rock') or \
             (user_choice == 'scissors' and bot_choice == 'paper'):
            result = "You win!"
            color = 0x00FF00
            reward = 25
        else:
            result = "I win!"
            color = 0xFF0000
            reward = 5
        
        # Give reward
        self.bot.db.update_user_coins(str(ctx.author.id), reward)
        
        embed = discord.Embed(
            title="🎮 Rock Paper Scissors",
            description=f"You chose **{user_choice}**\nI chose **{bot_choice}**\n\n{result}",
            color=color
        )
        embed.add_field(name="Reward", value=f"{reward} coins", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='guess')
    async def number_guessing(self, ctx, number: int = None):
        """Guess a number between 1-10"""
        if number is None:
            await ctx.send("🎲 Usage: `!guess <number 1-10>`")
            return
        
        if not 1 <= number <= 10:
            await ctx.send("❌ Number must be between 1 and 10!")
            return
        
        secret_number = random.randint(1, 10)
        
        if number == secret_number:
            reward = 100
            result = "🎉 Correct! You guessed it!"
            color = 0x00FF00
        else:
            reward = 10
            result = f"❌ Wrong! The number was {secret_number}"
            color = 0xFF0000
        
        self.bot.db.update_user_coins(str(ctx.author.id), reward)
        
        embed = discord.Embed(
            title="🎲 Number Guessing Game",
            description=result,
            color=color
        )
        embed.add_field(name="Reward", value=f"{reward} coins", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='trivia')
    async def trivia_command(self, ctx):
        """Answer trivia questions"""
        questions = [
            {"question": "What is the capital of France?", "answer": "paris", "options": ["London", "Berlin", "Paris", "Madrid"]},
            {"question": "How many planets are in our solar system?", "answer": "8", "options": ["7", "8", "9", "10"]},
            {"question": "What is 2 + 2?", "answer": "4", "options": ["3", "4", "5", "6"]},
            {"question": "What color do you get when you mix red and blue?", "answer": "purple", "options": ["Green", "Purple", "Orange", "Yellow"]},
            {"question": "What is the largest mammal?", "answer": "blue whale", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"]}
        ]
        
        question_data = random.choice(questions)
        
        embed = discord.Embed(
            title="🧠 Trivia Time!",
            description=question_data["question"],
            color=0x5865F2
        )
        
        for i, option in enumerate(question_data["options"], 1):
            embed.add_field(name=f"{i}. {option}", value="\u200b", inline=False)
        
        embed.set_footer(text="Type your answer in chat! (30 seconds)")
        
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            user_answer = await self.bot.wait_for('message', check=check, timeout=30)
            
            if user_answer.content.lower() == question_data["answer"]:
                reward = 50
                result = "🎉 Correct!"
                color = 0x00FF00
            else:
                reward = 10
                result = f"❌ Wrong! The answer was: {question_data['answer']}"
                color = 0xFF0000
            
            self.bot.db.update_user_coins(str(ctx.author.id), reward)
            
            embed = discord.Embed(
                title="🧠 Trivia Result",
                description=result,
                color=color
            )
            embed.add_field(name="Reward", value=f"{reward} coins", inline=True)
            
            await ctx.send(embed=embed)
            
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Time's up! The answer was: **{question_data['answer']}**")
    
    @commands.command(name='slots')
    async def slot_machine(self, ctx, bet: int = None):
        """Play the slot machine"""
        if bet is None:
            await ctx.send("🎰 Usage: `!slots <bet amount>`")
            return
        
        if bet <= 0:
            await ctx.send("❌ Bet must be positive!")
            return
        
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        if user_data.get('coins', 0) < bet:
            await ctx.send(f"💰 You don't have enough coins! You have {user_data.get('coins', 0):,}")
            return
        
        symbols = ['🍒', '🍋', '🍊', '🍇', '🔔', '💎', '7️⃣']
        
        # Spin the slots
        result = [random.choice(symbols) for _ in range(3)]
        
        # Check for wins
        if result[0] == result[1] == result[2]:
            # All three match
            if result[0] == '💎':
                multiplier = 10
            elif result[0] == '7️⃣':
                multiplier = 8
            else:
                multiplier = 5
            
            winnings = bet * multiplier
            self.bot.db.update_user_coins(user_id, winnings - bet)
            
            embed = discord.Embed(
                title="🎰 JACKPOT!",
                description=f"{''.join(result)}\n\nYou won **{winnings:,}** coins!",
                color=0x00FF00
            )
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            # Two match
            winnings = bet * 2
            self.bot.db.update_user_coins(user_id, winnings - bet)
            
            embed = discord.Embed(
                title="🎰 Small Win!",
                description=f"{''.join(result)}\n\nYou won **{winnings:,}** coins!",
                color=0xFFFF00
            )
        else:
            # No match
            self.bot.db.update_user_coins(user_id, -bet)
            
            embed = discord.Embed(
                title="🎰 No Luck!",
                description=f"{''.join(result)}\n\nYou lost **{bet:,}** coins!",
                color=0xFF0000
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='coinflip', aliases=['flip'])
    async def coinflip_command(self, ctx, bet: int = None, choice: str = None):
        """Flip a coin and bet on the outcome"""
        if bet is None or choice is None:
            await ctx.send("🪙 Usage: `!coinflip <bet> <heads/tails>`")
            return
        
        if choice.lower() not in ['heads', 'tails']:
            await ctx.send("❌ Choose 'heads' or 'tails'!")
            return
        
        user_id = str(ctx.author.id)
        user_data = self.bot.db.get_user(user_id)
        
        if user_data.get('coins', 0) < bet:
            await ctx.send(f"💰 You don't have enough coins! You have {user_data.get('coins', 0):,}")
            return
        
        result = random.choice(['heads', 'tails'])
        
        if choice.lower() == result:
            winnings = bet * 2
            self.bot.db.update_user_coins(user_id, winnings - bet)
            
            embed = discord.Embed(
                title="🪙 Coin Flip - You Win!",
                description=f"The coin landed on **{result}**!\nYou won **{winnings:,}** coins!",
                color=0x00FF00
            )
        else:
            self.bot.db.update_user_coins(user_id, -bet)
            
            embed = discord.Embed(
                title="🪙 Coin Flip - You Lost!",
                description=f"The coin landed on **{result}**!\nYou lost **{bet:,}** coins!",
                color=0xFF0000
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='dice')
    async def dice_roll(self, ctx, sides: int = 6):
        """Roll a dice"""
        if sides < 2:
            await ctx.send("❌ Dice must have at least 2 sides!")
            return
        
        if sides > 100:
            await ctx.send("❌ Maximum 100 sides!")
            return
        
        result = random.randint(1, sides)
        
        embed = discord.Embed(
            title=f"🎲 Dice Roll (d{sides})",
            description=f"You rolled a **{result}**!",
            color=0x5865F2
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GameCommands(bot))
