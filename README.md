# Kaala Billota - Advanced Discord Bot

A human-like conversational AI Discord bot with personality shifts, interactive configuration, and natural conversation capabilities.

## 🌟 Features

### 🤖 AI Features
- **Human-like conversation** - Responds naturally to messages, not just commands
- **Personality modes** - Switch between friendly, witty, casual, enthusiastic, and thoughtful
- **Groq Llama-3 integration** - Powered by Groq's fast LLM
- **Memory system** - Remembers conversation history
- **Natural mention handling** - Replaces Discord mentions with display names

### ⚙️ Configuration
- **Interactive `/config` command** - Modern embed-based configuration
- **Real-time settings** - Adjust chat frequency, personality, and features
- **Button-based UI** - Easy-to-use configuration panels
- **Admin controls** - Configure bot behavior from Discord

### �� Chat Features
- **Random participation** - Joins conversations naturally (configurable frequency)
- **Mention responses** - Always responds when mentioned
- **DM support** - Full conversation in DMs
- **Reaction system** - Adds natural reactions to responses
- **Rate limiting** - Prevents spam and abuse

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/nonamep-p/Discord-Bot-.git
cd Discord-Bot-

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" tab and create a bot
4. Copy the bot token to your `.env` file
5. Enable "Message Content Intent" in Bot settings
6. Use OAuth2 URL Generator to invite bot with permissions:
   - Send Messages
   - Read Message History
   - Embed Links
   - Use Slash Commands

### 4. Groq API Setup
1. Go to [Groq Console](https://console.groq.com/)
2. Create an account and get your API key
3. Add the key to your `.env` file

### 5. Run the Bot
```bash
python main.py
```

## 📋 Commands

### Configuration
- `/config` - Interactive configuration panel

### Chat Commands
- `!help` - Show all commands
- `!ping` - Check bot status
- `!balance` - Check coin balance
- `!daily` - Claim daily reward

### AI Commands
- `!chat [message]` - Direct AI chat
- `!roleplay [character]` - Switch personality mode

## ⚙️ Configuration

Use `/config` to access the interactive configuration panel:

### Chat Settings
- **Chat Frequency** - How often the bot joins random conversations
- **Random Chat** - Enable/disable random participation
- **Mention Only** - Only respond when mentioned

### Personality Settings
- **Friendly** - Warm and approachable
- **Witty** - Clever and humorous
- **Casual** - Relaxed and informal
- **Enthusiastic** - Energetic and excited
- **Thoughtful** - Deep and reflective

### Feature Settings
- **Reactions** - Enable/disable reaction emojis
- **Memory** - Conversation history (always enabled)
- **Personality Shifts** - Dynamic personality changes

## 🏗️ Architecture

```
├── main.py              # Entry point
├── bot.py               # Main bot class
├── api_client.py        # Groq API integration
├── personality.py       # Personality management
├── commands.py          # Command handlers
├── config_commands.py   # Interactive config
├── config.py           # Configuration management
├── database.py         # Data persistence
└── rate_limiter.py     # Rate limiting
```

## 🚀 Deployment

### Render (Recommended)
1. Fork this repository
2. Connect to Render
3. Set environment variables
4. Deploy automatically

### Railway
1. Connect your GitHub repo
2. Set environment variables
3. Deploy with Railway

### Local/Server
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DISCORD_BOT_TOKEN=your_token
export GROQ_API_KEY=your_key

# Run the bot
python main.py
```

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Discord bot token | ✅ |
| `GROQ_API_KEY` | Groq API key | ✅ |

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🐛 Troubleshooting

### Bot not responding
- Check if bot token is correct
- Verify bot has proper permissions
- Check if bot is online

### AI not working
- Verify Groq API key is valid
- Check API rate limits
- Ensure internet connectivity

### Configuration not working
- Make sure bot has slash command permissions
- Check if `/config` command is loaded
- Verify bot has embed permissions
