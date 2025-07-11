# Discord AI Bot

A feature-rich Discord bot with AI chat, image generation, GIF search, and multiple personas.

## Features

### 🤖 AI Features
- **Chat with AI**: Use `!chat <message>` to talk with AI using different personas
- **Image Generation**: Use `!image <prompt>` to generate images with DALL-E
- **Multiple Personas**: Switch between different AI personalities:
  - Default: Helpful assistant
  - Pirate: Swashbuckling pirate
  - Wizard: Mystical wizard
  - Robot: Futuristic AI
  - Chef: Passionate chef
  - Detective: Sharp detective

### 🎬 Media Features
- **GIF Search**: Use `!gif <search>` to find GIFs
- **Random Memes**: Use `!meme` to get random memes from Reddit

### 🔧 Utility Features
- **Server Info**: Use `!serverinfo` to get server statistics
- **User Info**: Use `!userinfo [user]` to get user information
- **Bot Status**: Use `!ping` and `!uptime` to check bot status

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- OpenAI API Key
- Giphy API Key (optional, for GIF features)

### 2. Installation

1. **Clone or download this project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Edit the `.env` file and add your API keys:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   GIPHY_API_KEY=your_giphy_api_key_here
   ```

### 3. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" tab and click "Add Bot"
4. Copy the bot token and add it to your `.env` file
5. Enable "Message Content Intent" in the Bot settings
6. Go to "OAuth2" > "URL Generator"
7. Select "bot" scope and the following permissions:
   - Send Messages
   - Read Message History
   - Embed Links
   - Attach Files
8. Use the generated URL to invite the bot to your server

### 4. API Keys Setup

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add it to your `.env` file

#### Giphy API Key (Optional)
1. Go to [Giphy for Developers](https://developers.giphy.com/)
2. Create an account and get your API key
3. Add it to your `.env` file

### 5. Running the Bot

```bash
python main.py
```

## Commands

### AI Commands
- `!chat <message>` - Chat with AI using current persona
- `!image <prompt>` - Generate image using DALL-E
- `!persona [name]` - Switch AI persona or list available personas

### Media Commands
- `!gif <search>` - Search for GIFs
- `!meme` - Get a random meme

### Utility Commands
- `!ping` - Check bot latency
- `!serverinfo` - Get server information
- `!userinfo [user]` - Get user information
- `!uptime` - Show bot uptime
- `!help` - Show all commands

## Hosting

### Option 1: Heroku (Platform)
1. Create a `Procfile` with: `worker: python main.py`
2. Push your code to Heroku
3. Set environment variables in Heroku dashboard

### Option 2: Oracle Cloud (Recommended VPS)
1. Create an Oracle Cloud Free Tier account
2. Create a Compute Instance with Ubuntu
3. SSH into your server
4. Clone your project and install dependencies
5. Create a systemd service for 24/7 uptime

#### Systemd Service Setup
Create `/etc/systemd/system/discord-bot.service`:
```ini
[Unit]
Description=Discord Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/discord-ai-bot
ExecStart=/home/ubuntu/discord-ai-bot/venv/bin/python3 /home/ubuntu/discord-ai-bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-bot.service
sudo systemctl start discord-bot.service
```

Check logs:
```bash
sudo journalctl -u discord-bot -f
```

## Project Structure

```
discord-ai-bot/
├── main.py                 # Main bot file
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
└── cogs/                 # Bot command modules
    ├── ai_commands.py    # AI and image generation commands
    ├── media_commands.py # GIF and meme commands
    └── utility_commands.py # Utility and info commands
```

## Troubleshooting

1. **Bot not responding**: Check if the bot token is correct and the bot is online
2. **AI commands not working**: Verify your OpenAI API key is valid and has credits
3. **GIF commands not working**: Check your Giphy API key or remove it to disable the feature
4. **Permission errors**: Make sure the bot has the required permissions in your Discord server

## License

This project is open source and available under the MIT License.
