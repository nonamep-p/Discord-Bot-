# Quick Start Guide

## 🚀 Get Your Bot Running in 5 Minutes

### 1. Get Your API Keys
- **Discord Bot Token**: [Discord Developer Portal](https://discord.com/developers/applications)
- **OpenAI API Key**: [OpenAI Platform](https://platform.openai.com/)
- **Giphy API Key**: [Giphy for Developers](https://developers.giphy.com/) (optional)

### 2. Configure Your Bot
Edit the `.env` file:
```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
GIPHY_API_KEY=your_giphy_api_key_here
```

### 3. Install and Run
```bash
# Run the setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Start the bot
python main.py
```

### 4. Invite Bot to Server
1. Go to Discord Developer Portal → Your App → OAuth2 → URL Generator
2. Select "bot" scope
3. Select permissions: Send Messages, Read Message History, Embed Links, Attach Files
4. Use the generated URL to invite bot to your server

## 🎯 Test Commands
- `!help` - See all commands
- `!chat Hello!` - Test AI chat
- `!persona pirate` - Switch to pirate persona
- `!image a cute cat` - Generate an image
- `!gif dancing` - Search for GIFs
- `!meme` - Get a random meme

## 🏠 Hosting Options

### Option A: Heroku (Easy)
1. Push code to GitHub
2. Connect to Heroku
3. Set environment variables in Heroku dashboard
4. Deploy!

### Option B: Oracle Cloud (Recommended)
1. Create Oracle Cloud Free Tier account
2. Create Ubuntu Compute Instance
3. SSH into server and clone your project
4. Run setup script
5. Use systemd service for 24/7 uptime:
   ```bash
   sudo cp discord-bot.service /etc/systemd/system/
   sudo systemctl enable discord-bot.service
   sudo systemctl start discord-bot.service
   ```

## 🆘 Need Help?
- Check the full README.md for detailed instructions
- Verify your API keys are correct
- Make sure the bot has proper permissions in Discord
- Check logs with `sudo journalctl -u discord-bot -f` (if using systemd)
