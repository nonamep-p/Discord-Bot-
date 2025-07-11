# Server Integration Guide - Avoiding Wick Detection

## 🛡️ Wick Protection Features

This bot includes several features to help avoid Wick bot detection:

### 1. Human-like Behavior
- **Random delays** between responses (1-5 seconds)
- **Typing indicators** to simulate human typing
- **Varied response lengths** and styles
- **Natural conversation patterns**

### 2. Security Features
- **Rate limiting** to prevent spam
- **Message sanitization** to remove suspicious content
- **Anti-spam protection**
- **Blocked word filtering**

### 3. Custom Personality Prompts
- Set your own personality prompt: `!prompt set <your prompt>`
- Clear custom prompt: `!prompt clear`
- Show current prompt: `!prompt show`

## 🚀 Adding to Your Server

### Step 1: Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section
4. Create a bot and copy the token
5. Set required permissions (see below)

### Step 2: Required Permissions
```
✅ Send Messages
✅ Read Message History
✅ Use Slash Commands
✅ Add Reactions
✅ Embed Links
✅ Attach Files
✅ Read Messages/View Channels
✅ Mention Everyone (optional)
```

### Step 3: Invite Link
Use this format for your invite link:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=2147483648&scope=bot
```

### Step 4: Environment Variables
Set these in your hosting platform:
```
DISCORD_BOT_TOKEN=your_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
```

## 🛡️ Wick Avoidance Tips

### 1. Bot Behavior
- **Don't respond too frequently** - The bot has built-in delays
- **Use natural language** - Avoid robotic responses
- **Add personality** - Use custom prompts to make it unique
- **Vary responses** - Don't always respond the same way

### 2. Server Settings
- **Role permissions** - Give bot appropriate roles
- **Channel permissions** - Limit bot to specific channels if needed
- **Message history** - Bot needs to read recent messages for context

### 3. Customization
- **Set custom prompt** - Make the bot unique to your server
- **Adjust chat frequency** - Lower frequency = less detection risk
- **Use mention-only mode** - Only respond when mentioned

## 🔧 Configuration Commands

### Basic Setup
```
!config - Open configuration panel
!prompt set <your prompt> - Set custom personality
!prompt clear - Remove custom prompt
```

### Example Custom Prompts
```
!prompt set You are a friendly gaming expert who loves helping with game strategies and always gives helpful tips
!prompt set You are a casual Discord user who loves memes, gaming, and having fun conversations
!prompt set You are a helpful community member who answers questions and engages in friendly discussions
```

## 🚨 Troubleshooting

### If Wick Kicks the Bot:
1. **Check permissions** - Ensure bot has required permissions
2. **Reduce activity** - Lower chat frequency in !config
3. **Use mention-only** - Set bot to only respond when mentioned
4. **Custom prompt** - Make responses more unique and human-like
5. **Server roles** - Give bot appropriate server roles

### Common Issues:
- **Bot not responding** - Check if it's online and has permissions
- **Permission errors** - Verify bot has required permissions
- **Rate limiting** - Bot has built-in rate limiting to avoid spam

## 📝 Best Practices

1. **Start conservative** - Use low chat frequency initially
2. **Monitor activity** - Watch how the bot behaves in your server
3. **Customize personality** - Make it fit your server's culture
4. **Test in small channels** - Start in a test channel first
5. **Adjust settings** - Use !config to fine-tune behavior

## �� Security Features

- **Message filtering** - Removes suspicious content
- **Rate limiting** - Prevents spam and abuse
- **User blocking** - Can block problematic users
- **Activity monitoring** - Tracks suspicious behavior

## 📞 Support

If you need help:
1. Check the bot's status with `!config`
2. Verify environment variables are set correctly
3. Check bot permissions in your server
4. Try reducing chat frequency if Wick is aggressive
