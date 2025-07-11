
import discord
from discord.ext import commands
import random
import asyncio
from typing import Dict, List

class MiniGamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.leaderboards = {}

    @commands.command(name='hangman')
    async def hangman(self, ctx):
        """Start a hangman game"""
        if ctx.channel.id in self.active_games:
            await ctx.send("🎮 There's already a game running in this channel!")
            return
            
        words = [
            'python', 'discord', 'programming', 'computer', 'keyboard',
            'adventure', 'challenge', 'mystery', 'treasure', 'rainbow'
        ]
        
        word = random.choice(words).upper()
        guessed = ['_'] * len(word)
        wrong_guesses = []
        max_wrong = 6
        
        self.active_games[ctx.channel.id] = {
            'type': 'hangman',
            'word': word,
            'guessed': guessed,
            'wrong_guesses': wrong_guesses,
            'max_wrong': max_wrong,
            'player': ctx.author.id
        }
        
        embed = discord.Embed(
            title="🎪 Hangman Game",
            description="Guess the word by typing letters!",
            color=discord.Color.purple()
        )
        
        embed.add_field(name="Word", value=' '.join(guessed), inline=False)
        embed.add_field(name="Wrong Guesses", value=f"{len(wrong_guesses)}/{max_wrong}", inline=True)
        embed.add_field(name="Letters Used", value="None yet", inline=True)
        
        hangman_art = self.get_hangman_art(len(wrong_guesses))
        embed.add_field(name="Gallows", value=f"```{hangman_art}```", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='connect4')
    async def connect_four(self, ctx, opponent: discord.Member = None):
        """Start a Connect 4 game"""
        if not opponent:
            await ctx.send("❌ Mention someone to play against!\nExample: `!connect4 @friend`")
            return
            
        if opponent.bot:
            await ctx.send("❌ You can't play against bots!")
            return
            
        if ctx.channel.id in self.active_games:
            await ctx.send("🎮 There's already a game running in this channel!")
            return
            
        # Initialize 6x7 board
        board = [['⚪' for _ in range(7)] for _ in range(6)]
        
        self.active_games[ctx.channel.id] = {
            'type': 'connect4',
            'board': board,
            'players': [ctx.author.id, opponent.id],
            'current_player': 0,
            'symbols': ['🔴', '🟡']
        }
        
        embed = discord.Embed(
            title="🔴 Connect 4 Game",
            description=f"{ctx.author.mention} 🔴 vs {opponent.mention} 🟡",
            color=discord.Color.red()
        )
        
        board_display = self.format_connect4_board(board)
        embed.add_field(name="Board", value=board_display, inline=False)
        embed.add_field(name="Current Turn", value=f"{ctx.author.mention} 🔴", inline=False)
        embed.add_field(name="How to Play", value="Type a number 1-7 to drop your piece!", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='tictactoe')
    async def tic_tac_toe(self, ctx, opponent: discord.Member = None):
        """Start a Tic Tac Toe game"""
        if not opponent:
            await ctx.send("❌ Mention someone to play against!\nExample: `!tictactoe @friend`")
            return
            
        if opponent.bot:
            await ctx.send("❌ You can't play against bots!")
            return
            
        if ctx.channel.id in self.active_games:
            await ctx.send("🎮 There's already a game running in this channel!")
            return
            
        # Initialize 3x3 board
        board = [['⬜' for _ in range(3)] for _ in range(3)]
        
        self.active_games[ctx.channel.id] = {
            'type': 'tictactoe',
            'board': board,
            'players': [ctx.author.id, opponent.id],
            'current_player': 0,
            'symbols': ['❌', '⭕']
        }
        
        embed = discord.Embed(
            title="❌ Tic Tac Toe",
            description=f"{ctx.author.mention} ❌ vs {opponent.mention} ⭕",
            color=discord.Color.blue()
        )
        
        board_display = self.format_tictactoe_board(board)
        embed.add_field(name="Board", value=board_display, inline=False)
        embed.add_field(name="Current Turn", value=f"{ctx.author.mention} ❌", inline=False)
        embed.add_field(name="How to Play", value="Type position 1-9 (like a numpad)", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='snake')
    async def snake_game(self, ctx):
        """Start a simple Snake game"""
        if ctx.channel.id in self.active_games:
            await ctx.send("🎮 There's already a game running in this channel!")
            return
            
        # Initialize 8x8 grid
        size = 8
        snake = [(size//2, size//2)]  # Start in center
        direction = (0, 1)  # Start moving right
        food = self.generate_food(snake, size)
        score = 0
        
        self.active_games[ctx.channel.id] = {
            'type': 'snake',
            'snake': snake,
            'direction': direction,
            'food': food,
            'score': score,
            'size': size,
            'player': ctx.author.id,
            'game_over': False
        }
        
        embed = discord.Embed(
            title="🐍 Snake Game",
            description="Use reactions to control the snake!",
            color=discord.Color.green()
        )
        
        grid = self.format_snake_board(snake, food, size)
        embed.add_field(name="Game Board", value=grid, inline=False)
        embed.add_field(name="Score", value=f"🏆 {score}", inline=True)
        embed.add_field(name="Controls", value="⬆️⬇️⬅️➡️", inline=True)
        
        message = await ctx.send(embed=embed)
        
        # Add control reactions
        for emoji in ['⬆️', '⬇️', '⬅️', '➡️']:
            await message.add_reaction(emoji)
            
        self.active_games[ctx.channel.id]['message_id'] = message.id

    def get_hangman_art(self, wrong_count):
        """Get hangman ASCII art based on wrong guesses"""
        stages = [
            "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n========="
        ]
        return stages[min(wrong_count, len(stages) - 1)]

    def format_connect4_board(self, board):
        """Format Connect 4 board for display"""
        board_str = "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣\n"
        for row in board:
            board_str += ''.join(row) + "\n"
        return board_str

    def format_tictactoe_board(self, board):
        """Format Tic Tac Toe board for display"""
        board_str = ""
        for i, row in enumerate(board):
            board_str += ''.join(row) + "\n"
        return board_str

    def format_snake_board(self, snake, food, size):
        """Format Snake game board"""
        grid = [['⬛' for _ in range(size)] for _ in range(size)]
        
        # Place food
        grid[food[0]][food[1]] = '🍎'
        
        # Place snake
        for i, (row, col) in enumerate(snake):
            if i == 0:  # Head
                grid[row][col] = '🟢'
            else:  # Body
                grid[row][col] = '🟡'
                
        return '\n'.join(''.join(row) for row in grid)

    def generate_food(self, snake, size):
        """Generate food position for snake game"""
        while True:
            pos = (random.randint(0, size-1), random.randint(0, size-1))
            if pos not in snake:
                return pos

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle game moves"""
        if message.author.bot or message.channel.id not in self.active_games:
            return
            
        game = self.active_games[message.channel.id]
        
        if game['type'] == 'hangman' and message.author.id == game['player']:
            await self.handle_hangman_guess(message, game)
        elif game['type'] == 'connect4':
            await self.handle_connect4_move(message, game)
        elif game['type'] == 'tictactoe':
            await self.handle_tictactoe_move(message, game)

    async def handle_hangman_guess(self, message, game):
        """Handle hangman letter guesses"""
        guess = message.content.upper().strip()
        
        if len(guess) != 1 or not guess.isalpha():
            return
            
        if guess in game['guessed'] or guess in game['wrong_guesses']:
            await message.channel.send(f"You already guessed '{guess}'!")
            return
            
        if guess in game['word']:
            # Correct guess
            for i, letter in enumerate(game['word']):
                if letter == guess:
                    game['guessed'][i] = letter
                    
            if '_' not in game['guessed']:
                # Won!
                embed = discord.Embed(
                    title="🎉 You Won!",
                    description=f"The word was: **{game['word']}**",
                    color=discord.Color.green()
                )
                await message.channel.send(embed=embed)
                del self.active_games[message.channel.id]
                return
        else:
            # Wrong guess
            game['wrong_guesses'].append(guess)
            
            if len(game['wrong_guesses']) >= game['max_wrong']:
                # Lost!
                embed = discord.Embed(
                    title="💀 Game Over!",
                    description=f"The word was: **{game['word']}**",
                    color=discord.Color.red()
                )
                hangman_art = self.get_hangman_art(len(game['wrong_guesses']))
                embed.add_field(name="Final State", value=f"```{hangman_art}```", inline=False)
                await message.channel.send(embed=embed)
                del self.active_games[message.channel.id]
                return
        
        # Update game display
        embed = discord.Embed(
            title="🎪 Hangman Game",
            description="Guess the word by typing letters!",
            color=discord.Color.purple()
        )
        
        embed.add_field(name="Word", value=' '.join(game['guessed']), inline=False)
        embed.add_field(name="Wrong Guesses", value=f"{len(game['wrong_guesses'])}/{game['max_wrong']}", inline=True)
        
        used_letters = list(set([l for l in game['guessed'] if l != '_'] + game['wrong_guesses']))
        embed.add_field(name="Letters Used", value=', '.join(sorted(used_letters)) if used_letters else "None", inline=True)
        
        hangman_art = self.get_hangman_art(len(game['wrong_guesses']))
        embed.add_field(name="Gallows", value=f"```{hangman_art}```", inline=False)
        
        await message.channel.send(embed=embed)

    async def handle_connect4_move(self, message, game):
        """Handle Connect 4 moves"""
        try:
            col = int(message.content) - 1
            if col < 0 or col > 6:
                return
        except ValueError:
            return
            
        current_player_id = game['players'][game['current_player']]
        if message.author.id != current_player_id:
            return
            
        # Check if column is full
        if game['board'][0][col] != '⚪':
            await message.channel.send("❌ That column is full!")
            return
            
        # Drop piece
        for row in range(5, -1, -1):
            if game['board'][row][col] == '⚪':
                game['board'][row][col] = game['symbols'][game['current_player']]
                break
                
        # Check for win
        if self.check_connect4_win(game['board'], row, col, game['symbols'][game['current_player']]):
            winner = self.bot.get_user(current_player_id)
            embed = discord.Embed(
                title="🎉 Connect 4 Winner!",
                description=f"{winner.mention} wins!",
                color=discord.Color.gold()
            )
            board_display = self.format_connect4_board(game['board'])
            embed.add_field(name="Final Board", value=board_display, inline=False)
            await message.channel.send(embed=embed)
            del self.active_games[message.channel.id]
            return
            
        # Switch players
        game['current_player'] = 1 - game['current_player']
        
        # Update display
        current_user = self.bot.get_user(game['players'][game['current_player']])
        embed = discord.Embed(
            title="🔴 Connect 4 Game",
            color=discord.Color.red()
        )
        
        board_display = self.format_connect4_board(game['board'])
        embed.add_field(name="Board", value=board_display, inline=False)
        embed.add_field(name="Current Turn", value=f"{current_user.mention} {game['symbols'][game['current_player']]}", inline=False)
        
        await message.channel.send(embed=embed)

    def check_connect4_win(self, board, row, col, symbol):
        """Check if there's a Connect 4 win"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            
            # Check positive direction
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == symbol:
                count += 1
                r, c = r + dr, c + dc
                
            # Check negative direction
            r, c = row - dr, col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == symbol:
                count += 1
                r, c = r - dr, c - dc
                
            if count >= 4:
                return True
                
        return False

    async def handle_tictactoe_move(self, message, game):
        """Handle Tic Tac Toe moves"""
        try:
            pos = int(message.content)
            if pos < 1 or pos > 9:
                return
        except ValueError:
            return
            
        current_player_id = game['players'][game['current_player']]
        if message.author.id != current_player_id:
            return
            
        # Convert position to row, col
        row, col = (pos - 1) // 3, (pos - 1) % 3
        
        if game['board'][row][col] != '⬜':
            await message.channel.send("❌ That position is already taken!")
            return
            
        # Make move
        game['board'][row][col] = game['symbols'][game['current_player']]
        
        # Check for win
        if self.check_tictactoe_win(game['board'], game['symbols'][game['current_player']]):
            winner = self.bot.get_user(current_player_id)
            embed = discord.Embed(
                title="🎉 Tic Tac Toe Winner!",
                description=f"{winner.mention} wins!",
                color=discord.Color.gold()
            )
            board_display = self.format_tictactoe_board(game['board'])
            embed.add_field(name="Final Board", value=board_display, inline=False)
            await message.channel.send(embed=embed)
            del self.active_games[message.channel.id]
            return
            
        # Check for tie
        if all(cell != '⬜' for row in game['board'] for cell in row):
            embed = discord.Embed(
                title="🤝 Tie Game!",
                description="It's a draw!",
                color=discord.Color.yellow()
            )
            board_display = self.format_tictactoe_board(game['board'])
            embed.add_field(name="Final Board", value=board_display, inline=False)
            await message.channel.send(embed=embed)
            del self.active_games[message.channel.id]
            return
            
        # Switch players
        game['current_player'] = 1 - game['current_player']
        
        # Update display
        current_user = self.bot.get_user(game['players'][game['current_player']])
        embed = discord.Embed(
            title="❌ Tic Tac Toe",
            color=discord.Color.blue()
        )
        
        board_display = self.format_tictactoe_board(game['board'])
        embed.add_field(name="Board", value=board_display, inline=False)
        embed.add_field(name="Current Turn", value=f"{current_user.mention} {game['symbols'][game['current_player']]}", inline=False)
        
        await message.channel.send(embed=embed)

    def check_tictactoe_win(self, board, symbol):
        """Check if there's a Tic Tac Toe win"""
        # Check rows
        for row in board:
            if all(cell == symbol for cell in row):
                return True
                
        # Check columns
        for col in range(3):
            if all(board[row][col] == symbol for row in range(3)):
                return True
                
        # Check diagonals
        if all(board[i][i] == symbol for i in range(3)):
            return True
        if all(board[i][2-i] == symbol for i in range(3)):
            return True
            
        return False

async def setup(bot):
    await bot.add_cog(MiniGamesCog(bot))
