# 🤖 Kaala Billota - Advanced Disc  ord Bot

A human-like Discord chatbot with custom personality prompts, security features, and Wick protection.

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

### 🎮 Interactive Configuration
- `!config` - Interactive configuration panel
- Chat frequency adjustment
- Personality mode selection
- Feature toggles
- Custom prompt management

### 💬 Natural Conversation
- Responds to mentions, DMs, and name calls
- Random chat participation
- Memory of conversation history
- Human-like typing indicators
- Natural response delays

## �� Quick Start

### 1. Environment Setup
```bash
# Required environment variables
DISCORD_BOT_TOKEN=your_discord_bot_token
GROQ_API_KEY=your_groq_api_key
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

- No hardcoded tokens
- Environment variable protection
- Message sanitization
- Rate limiting
- Anti-spam measures
- Suspicious activity monitoring

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
