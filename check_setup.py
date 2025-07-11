
import os
from dotenv import load_dotenv

def check_setup():
    """Check if all required components are set up"""
    load_dotenv()
    
    print("🔍 Checking bot setup...")
    
    # Check Discord token
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        print("✅ Discord bot token found")
        if len(token) > 50:
            print(f"   Token preview: {token[:20]}...{token[-10:]}")
        else:
            print("⚠️  Token seems short - make sure it's correct")
    else:
        print("❌ Discord bot token not found!")
        print("   Please add DISCORD_BOT_TOKEN to your Secrets")
        return False
    
    # Check API token (optional)
    api_token = os.getenv('GROQ_API_KEY') or os.getenv('OPENAI_API_KEY')
    if api_token:
        print("✅ API token found for AI features")
    else:
        print("⚠️  No API token found - AI features may be limited")
        print("   Add GROQ_API_KEY or OPENAI_API_KEY for full functionality")
    
    # Check files
    required_files = ['bot.py', 'commands.py', 'database.py', 'config.py']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing!")
            return False
    
    print("\n🎉 Setup looks good! Try running the bot now.")
    return True

if __name__ == "__main__":
    check_setup()
