#!/bin/bash

echo "�� Discord AI Bot Setup Script"
echo "=============================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it with your API keys."
    echo "Example .env file:"
    echo "DISCORD_BOT_TOKEN=your_discord_bot_token_here"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo "GIPHY_API_KEY=your_giphy_api_key_here"
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 To run the bot:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the bot: python main.py"
echo ""
echo "📖 For hosting instructions, see README.md"
