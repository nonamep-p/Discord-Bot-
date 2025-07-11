# 🤖 Kaala Billota - Advanced Discord Bot

A human-like Discord chatbot with custom personality prompts, security features, Wick protection, real GIF search, and advanced analytics.

## ✨ Features

### 🎭 Custom Personality Prompts
- Set your own personality prompt: `!prompt set <your prompt>`
- Clear custom prompt: `!prompt clear`
- Show current prompt: `!prompt show`
- Maintains mood shifting and personality modes

### 🛡️ Security & Protection
- **Wick bot protection** - Human-like behavior to avoid detection
- **Rate limiting** - Prevents spam and abuse
- **Message sanitization** - Removes suspicious content
- **Anti-spam protection** - Monitors message frequency
- **Blocked word filtering** - Prevents token leaks
- **Advanced security toggles** - Enable/disable advanced security features
- **User blocking capabilities**

### 📊 Advanced Analytics & Policy Compliance
- **Analytics/statistics** - Real-time bot and server analytics
- **Discord policy compliance status** - Live compliance checks and status

### 🎮 Interactive Configuration
- `!config` - Interactive configuration panel
- Chat frequency adjustment
- Personality mode selection
- Feature toggles
- Custom prompt management
- **Server-specific config** - All settings are now per-server

### 💬 Natural Conversation
- Responds to mentions, DMs, and name calls
- Random chat participation
- Memory of conversation history
- Human-like typing indicators
- Natural response delays

### 🎨 Image & GIF Generation
- `!image <prompt>` - Persona-aware fallback (no real image generation; bot responds in-character with a description)
- `!gif <search>` - **Real GIF search powered by GIPHY API** (requires GIPHY API key in `.env`)
- *Add your API keys to enable real GIF generation. Image generation is fallback only.*

##  Quick Start

### 1. Environment Setup
```bash
# Required environment variables (store in a .env file, never commit secrets)
DISCORD_BOT_TOKEN=your_discord_bot_token
GROQ_API_KEY=your_groq_api_key
GIPHY_API_KEY=your_giphy_api_key
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Bot
```bash
python3 bot.py
```

## 📋 Commands

### Configuration
- `!config` - Open interactive configuration panel
- `!prompt set <prompt>` - Set custom personality prompt
- `!prompt clear` - Clear custom prompt
- `!prompt show` - Show current prompt
- `!image <prompt>` - Persona-aware fallback (no real images)
- `!gif <search>` - Real GIF search (requires GIPHY API key)

### Example Custom Prompts
```
!prompt set You are a friendly gaming expert who loves helping with game strategies
!prompt set You are a casual Discord user who loves memes and fun conversations
!prompt set You are a helpful community member who answers questions thoughtfully
```

## 🛡️ Wick Protection

This bot includes several features to avoid Wick bot detection:

- **Human-like delays** between responses
- **Typing indicators** to simulate human behavior
- **Varied response styles** and lengths
- **Natural conversation patterns**
- **Rate limiting** to prevent spam
- **Customizable chat frequency**

## 🔧 Configuration

### Chat Settings
- **Chat Frequency**: 1-50% chance to join random conversations
- **Random Chat**: Enable/disable random participation
- **Mention Only**: Only respond when mentioned
- **Reactions**: Enable/disable random reactions

### Personality Modes
- **Friendly**: Warm and approachable
- **Witty**: Clever and humorous
- **Casual**: Relaxed and informal
- **Enthusiastic**: Energetic and excited
- **Thoughtful**: Deep and reflective

### Security Features
- **Message filtering** for suspicious content
- **Rate limiting** to prevent abuse
- **Anti-spam protection**
- **User blocking capabilities**
- **Advanced security toggles**

## 📁 Project Structure

```
Discord-Bot-/
├── bot.py                 # Main bot file
├── personality.py         # Personality management
├── config_commands.py     # Interactive configuration
├── custom_prompt_commands.py # Custom prompt commands
├── security.py           # Security features
├── wick_protection.py    # Wick avoidance
├── database.py           # Data storage
├── api_client.py         # API integration
├── rate_limiter.py       # Rate limiting
├── requirements.txt      # Dependencies
├── deploy.sh            # Deployment script
└── SERVER_INTEGRATION_GUIDE.md # Wick avoidance guide
```

## 🔒 Security

- No hardcoded tokens or API keys in code or config files
- **Secrets must be stored in `.env` and never committed**
- Environment variable protection
- Message sanitization
- Rate limiting
- Anti-spam measures
- Suspicious activity monitoring
- **GitHub push protection and secret scanning are enabled**

## 🚨 Troubleshooting

### Common Issues
1. **Bot not responding**: Check permissions and token
2. **Wick kicks bot**: Reduce chat frequency, use custom prompts
3. **Permission errors**: Verify bot has required permissions
4. **Rate limiting**: Bot has built-in protection

### Getting Help
1. Check `!config` for current settings
2. Verify environment variables
3. Check bot permissions in server
4. Review SERVER_INTEGRATION_GUIDE.md

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting features
- Improving documentation
- Adding security enhancements

---

## 🔒 Privacy & Compliance

- This bot does **not collect or share personal data**.
- All features comply with [Discord’s Terms of Service](https://discord.com/terms) and [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy).
- Conversation history and user coins are stored securely and never shared.
- The bot does not send unsolicited DMs or spam.
- No NSFW, harmful, or illegal content is allowed.
