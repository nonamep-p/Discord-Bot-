#!/bin/bash

echo "🚀 Deploying Discord Bot with Security Features..."

# Check if required environment variables are set
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "❌ Error: DISCORD_BOT_TOKEN environment variable not set!"
    echo "Please set your Discord bot token in the environment variables."
    exit 1
fi

if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ Error: GROQ_API_KEY environment variable not set!"
    echo "Please set your Groq API key in the environment variables."
    exit 1
fi

echo "✅ Environment variables check passed"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Security check - verify no hardcoded tokens
echo "🔒 Running security checks..."
if grep -r "discord_token\|bot_token\|api_key" . --exclude-dir=venv --exclude-dir=__pycache__ --exclude=*.pyc; then
    echo "⚠️  Warning: Potential hardcoded tokens found in code!"
    echo "Please ensure all tokens are stored in environment variables."
fi

# Create necessary directories
mkdir -p logs
mkdir -p data

# Set proper permissions
chmod 600 *.py
chmod 644 requirements.txt
chmod 644 *.md

echo "✅ Security setup complete"

# Start the bot
echo "🤖 Starting Discord bot..."
python3 bot.py
