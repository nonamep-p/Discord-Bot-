#!/usr/bin/env python3
"""
Kaala Billota - Advanced Discord Bot
A human-like conversational AI bot with personality shifts and interactive configuration.
"""

import asyncio
import os
from dotenv import load_dotenv
from bot import setup_bot

# Load environment variables
load_dotenv()

async def main():
    """Main entry point"""
    print("🤖 Starting Kaala Billota Discord Bot...")
    print("📝 Features:")
    print("   • Human-like conversation")
    print("   • Interactive /config command")
    print("   • Personality modes")
    print("   • Groq Llama-3 integration")
    print("   • Natural mention handling")
    print("   • Random chat participation")
    print()
    
    await setup_bot()

if __name__ == "__main__":
    asyncio.run(main())
