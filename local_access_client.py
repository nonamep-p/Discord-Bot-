#!/usr/bin/env python3
"""
Local client to access your Replit Discord bot remotely
Run this on your local machine to connect to your bot
"""

import requests
import os
import json
import time
from datetime import datetime

class BotRemoteClient:
    def __init__(self, replit_url):
        self.base_url = f"https://{replit_url}:8080"
        self.session = requests.Session()
        
    def get_status(self):
        """Get bot status"""
        try:
            response = self.session.get(f"{self.base_url}/api/status")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_file(self, filename):
        """Download a file from the bot"""
        try:
            response = self.session.get(f"{self.base_url}/api/file/{filename}")
            return response.text
        except Exception as e:
            return f"Error: {e}"
    
    def save_file(self, filename, content):
        """Upload a file to the bot"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/file/{filename}",
                data=content,
                headers={'Content-Type': 'text/plain'}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def execute_command(self, command):
        """Execute a command on the bot server"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/command",
                json={"command": command}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def sync_files_down(self, local_dir):
        """Download all bot files to local directory"""
        files = ['bot.py', 'commands.py', 'personality.py', 'api_client.py', 
                'config.py', 'database.py', 'rate_limiter.py']
        
        os.makedirs(local_dir, exist_ok=True)
        
        for file in files:
            content = self.get_file(file)
            if not content.startswith("Error:"):
                with open(os.path.join(local_dir, file), 'w') as f:
                    f.write(content)
                print(f"✅ Downloaded {file}")
            else:
                print(f"❌ Failed to download {file}: {content}")
    
    def sync_files_up(self, local_dir):
        """Upload all local files to bot server"""
        for file in os.listdir(local_dir):
            if file.endswith('.py'):
                with open(os.path.join(local_dir, file), 'r') as f:
                    content = f.read()
                
                result = self.save_file(file, content)
                if result.get('success'):
                    print(f"✅ Uploaded {file}")
                else:
                    print(f"❌ Failed to upload {file}: {result.get('error', 'Unknown error')}")

def main():
    print("Discord Bot Remote Client")
    print("=" * 30)
    
    replit_url = input("Enter your Replit URL (e.g., mybot.username.replit.dev): ").strip()
    if not replit_url:
        print("No URL provided, exiting...")
        return
    
    client = BotRemoteClient(replit_url)
    
    while True:
        print("\nOptions:")
        print("1. Check bot status")
        print("2. Download specific file")
        print("3. Upload specific file")
        print("4. Execute command")
        print("5. Sync all files DOWN (bot → local)")
        print("6. Sync all files UP (local → bot)")
        print("7. Edit file locally and upload")
        print("8. Exit")
        
        choice = input("\nChoose option (1-8): ").strip()
        
        if choice == "1":
            status = client.get_status()
            print(f"\nBot Status: {json.dumps(status, indent=2)}")
            
        elif choice == "2":
            filename = input("File to download: ").strip()
            content = client.get_file(filename)
            print(f"\n--- {filename} ---")
            print(content)
            
        elif choice == "3":
            filename = input("File to upload: ").strip()
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    content = f.read()
                result = client.save_file(filename, content)
                print(f"Upload result: {result}")
            else:
                print("File not found locally!")
                
        elif choice == "4":
            command = input("Command to execute: ").strip()
            result = client.execute_command(command)
            print(f"Command output: {result.get('output', result)}")
            
        elif choice == "5":
            local_dir = input("Local directory to sync to (default: ./bot_files): ").strip()
            if not local_dir:
                local_dir = "./bot_files"
            client.sync_files_down(local_dir)
            
        elif choice == "6":
            local_dir = input("Local directory to sync from (default: ./bot_files): ").strip()
            if not local_dir:
                local_dir = "./bot_files"
            if os.path.exists(local_dir):
                client.sync_files_up(local_dir)
            else:
                print("Local directory not found!")
                
        elif choice == "7":
            filename = input("File to edit: ").strip()
            # Download file
            content = client.get_file(filename)
            
            # Save locally
            with open(f"temp_{filename}", 'w') as f:
                f.write(content)
            
            print(f"File saved as temp_{filename}")
            input("Edit the file and press Enter when done...")
            
            # Upload back
            with open(f"temp_{filename}", 'r') as f:
                new_content = f.read()
            
            result = client.save_file(filename, new_content)
            print(f"Upload result: {result}")
            
            # Cleanup
            os.remove(f"temp_{filename}")
            
        elif choice == "8":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()