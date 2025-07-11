import os

class Config:
    """Configuration settings for the Discord bot"""
    
    def __init__(self):
        # API Keys
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY', 'default_deepseek_key')
        self.giphy_api_key = os.getenv('GIPHY_API_KEY', 'default_giphy_key')
        
        # Bot settings
        self.command_prefix = '!'
        self.max_message_length = 2000
        
        # Economy settings
        self.starting_coins = 1000
        self.daily_reward = 100
        
        # Command costs
        self.command_costs = {
            'chat': 10,
            'image': 50,
            'gif': 5,
            'daily': 0,
            'balance': 0,
            'gift': 0,
            'limits': 0,
            'ping': 0,
            'help': 0,
            'roleplay': 0
        }
        
        # Rate limits
        self.rate_limits = {
            'api_calls_per_hour': 50,
            'images_per_day': 10,
            'conversations_per_minute': 5
        }
        
        # File paths
        self.data_dir = 'data'
        self.users_file = f'{self.data_dir}/users.json'
        self.usage_file = f'{self.data_dir}/usage.json'
        self.conversations_file = f'{self.data_dir}/conversations.json'
        
        # API URLs
        self.deepseek_api_url = 'https://api.deepseek.com/v1/chat/completions'
        self.giphy_api_url = 'https://api.giphy.com/v1/gifs/search'
        
        # Personality settings
        self.max_conversation_history = 5
        self.personality_traits = [
            "funny and witty",
            "helpful but slightly sarcastic", 
            "friendly and casual",
            "uses emojis naturally",
            "remembers conversation context",
            "acts like a real person, not a formal assistant"
        ]
        
    def get_command_cost(self, command):
        """Get the coin cost for a command"""
        return self.command_costs.get(command, 0)
