import sqlite3
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class Database:
    """Simple SQLite database for user data and conversations"""
    
    def __init__(self):
        self.db_path = "bot_data.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    coins INTEGER DEFAULT 1000,
                    personality_mode TEXT DEFAULT 'friendly',
                    total_commands INTEGER DEFAULT 0,
                    last_daily TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    user_message TEXT,
                    bot_response TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Usage tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage (
                    user_id TEXT,
                    date TEXT,
                    hourly_calls INTEGER DEFAULT 0,
                    images_today INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, date)
                )
            ''')
            
            # Economy transactions table for better tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    transaction_type TEXT,
                    amount INTEGER,
                    balance_after INTEGER,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def get_user(self, user_id: str) -> Dict:
        """Get or create user data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM users WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            
            if result:
                return {
                    'user_id': result[0],
                    'coins': result[1],
                    'personality_mode': result[2],
                    'total_commands': result[3],
                    'last_daily': result[4],
                    'created_at': result[5]
                }
            else:
                # Create new user
                cursor.execute('''
                    INSERT INTO users (user_id, coins, personality_mode)
                    VALUES (?, 1000, 'friendly')
                ''', (user_id,))
                conn.commit()
                
                return {
                    'user_id': user_id,
                    'coins': 1000,
                    'personality_mode': 'friendly',
                    'total_commands': 0,
                    'last_daily': None,
                    'created_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return {'user_id': user_id, 'coins': 1000, 'personality_mode': 'friendly'}
        finally:
            conn.close()
    
    def add_conversation(self, user_id: str, user_message: str, bot_response: str):
        """Add conversation to history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversations (user_id, user_message, bot_response)
                VALUES (?, ?, ?)
            ''', (user_id, user_message, bot_response))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error adding conversation: {e}")
        finally:
            conn.close()
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_message, bot_response FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            return [{'user_message': row[0], 'bot_response': row[1]} for row in results]
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
        finally:
            conn.close()
    
    def spend_coins(self, user_id: str, amount: int) -> bool:
        """Spend coins if user has enough"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # First check if user has enough coins
            cursor.execute('''
                SELECT coins FROM users WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if not result or result[0] < amount:
                conn.close()
                return False
            
            current_balance = result[0]
            new_balance = current_balance - amount
            
            # Update coins
            cursor.execute('''
                UPDATE users SET coins = ?
                WHERE user_id = ?
            ''', (new_balance, user_id))
            
            # Log transaction
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
                VALUES (?, 'spend', ?, ?)
            ''', (user_id, -amount, new_balance))
            
            conn.commit()
            conn.close()
            
            logger.info(f"User {user_id} spent {amount} coins. New balance: {new_balance}")
            return True
            
        except Exception as e:
            logger.error(f"Error spending coins: {e}")
            return False
    
    def add_coins(self, user_id: str, amount: int):
        """Add coins to user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current balance
            cursor.execute('''
                SELECT coins FROM users WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            current_balance = result[0] if result else 0
            new_balance = current_balance + amount
            
            # Update coins
            cursor.execute('''
                UPDATE users SET coins = ?
                WHERE user_id = ?
            ''', (new_balance, user_id))
            
            # Log transaction
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
                VALUES (?, 'add', ?, ?)
            ''', (user_id, amount, new_balance))
            
            conn.commit()
            conn.close()
            
            logger.info(f"User {user_id} received {amount} coins. New balance: {new_balance}")
            
        except Exception as e:
            logger.error(f"Error adding coins: {e}")
    
    def transfer_coins(self, sender_id: str, receiver_id: str, amount: int) -> bool:
        """Transfer coins between users"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if sender has enough coins
            cursor.execute('''
                SELECT coins FROM users WHERE user_id = ?
            ''', (sender_id,))
            
            sender_result = cursor.fetchone()
            if not sender_result or sender_result[0] < amount:
                conn.close()
                return False
            
            # Check if receiver exists, create if not
            cursor.execute('''
                SELECT coins FROM users WHERE user_id = ?
            ''', (receiver_id,))
            
            receiver_result = cursor.fetchone()
            if not receiver_result:
                # Create receiver user
                cursor.execute('''
                    INSERT INTO users (user_id, coins, personality_mode)
                    VALUES (?, 0, 'friendly')
                ''', (receiver_id,))
                receiver_balance = 0
            else:
                receiver_balance = receiver_result[0]
            
            sender_balance = sender_result[0]
            
            # Transfer coins
            cursor.execute('''
                UPDATE users SET coins = ? WHERE user_id = ?
            ''', (sender_balance - amount, sender_id))
            
            cursor.execute('''
                UPDATE users SET coins = ? WHERE user_id = ?
            ''', (receiver_balance + amount, receiver_id))
            
            # Log transactions
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
                VALUES (?, 'transfer_sent', ?, ?)
            ''', (sender_id, -amount, sender_balance - amount))
            
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
                VALUES (?, 'transfer_received', ?, ?)
            ''', (receiver_id, amount, receiver_balance + amount))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Transfer: {sender_id} -> {receiver_id}: {amount} coins")
            return True
            
        except Exception as e:
            logger.error(f"Error transferring coins: {e}")
            return False
    
    def can_claim_daily(self, user_id: str) -> bool:
        """Check if user can claim daily reward"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT last_daily FROM users WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result or not result[0]:
                return True
            
            # Parse the last daily time and check if 24 hours have passed
            last_daily = datetime.fromisoformat(result[0])
            now = datetime.now(timezone.utc)
            
            # Check if it's been more than 24 hours since last claim
            time_diff = now - last_daily.replace(tzinfo=timezone.utc)
            return time_diff.total_seconds() >= 86400  # 24 hours in seconds
            
        except Exception as e:
            logger.error(f"Error checking daily claim: {e}")
            return True
    
    def claim_daily(self, user_id: str) -> int:
        """Claim daily reward and return new balance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current balance
            cursor.execute('''
                SELECT coins FROM users WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            current_balance = result[0] if result else 0
            new_balance = current_balance + 100
            
            # Update coins and last daily time
            cursor.execute('''
                UPDATE users 
                SET coins = ?, last_daily = ?
                WHERE user_id = ?
            ''', (new_balance, datetime.now(timezone.utc).isoformat(), user_id))
            
            # Log transaction
            cursor.execute('''
                INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
                VALUES (?, 'daily_reward', ?, ?)
            ''', (user_id, 100, new_balance))
            
            conn.commit()
            conn.close()
            
            logger.info(f"User {user_id} claimed daily reward. New balance: {new_balance}")
            return new_balance
            
        except Exception as e:
            logger.error(f"Error claiming daily: {e}")
            return 1000
    
    def get_transaction_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's recent transaction history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT transaction_type, amount, balance_after, timestamp 
                FROM transactions 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'type': row[0],
                    'amount': row[1],
                    'balance_after': row[2],
                    'timestamp': row[3]
                }
                for row in results
            ]
            
        except Exception as e:
            logger.error(f"Error getting transaction history: {e}")
            return []
    
    def set_personality_mode(self, user_id: str, mode: str):
        """Set user's personality mode"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET personality_mode = ?
                WHERE user_id = ?
            ''', (mode, user_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error setting personality mode: {e}")
    
    def get_usage_data(self, user_id: str) -> Dict:
        """Get user's usage data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT hourly_calls, images_today FROM usage
                WHERE user_id = ? AND date = ?
            ''', (user_id, today))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'hourly_calls': result[0],
                    'images_today': result[1]
                }
            else:
                return {'hourly_calls': 0, 'images_today': 0}
                
        except Exception as e:
            logger.error(f"Error getting usage data: {e}")
            return {'hourly_calls': 0, 'images_today': 0}
    
    def update_usage(self, user_id: str, usage_type: str):
        """Update usage tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            if usage_type == 'api_call':
                cursor.execute('''
                    INSERT OR REPLACE INTO usage (user_id, date, hourly_calls)
                    VALUES (?, ?, COALESCE(
                        (SELECT hourly_calls FROM usage WHERE user_id = ? AND date = ?), 0
                    ) + 1)
                ''', (user_id, today, user_id, today))
            elif usage_type == 'image':
                cursor.execute('''
                    INSERT OR REPLACE INTO usage (user_id, date, images_today)
                    VALUES (?, ?, COALESCE(
                        (SELECT images_today FROM usage WHERE user_id = ? AND date = ?), 0
                    ) + 1)
                ''', (user_id, today, user_id, today))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating usage: {e}")
    
    def reset_user_data(self, user_id: str):
        """Reset user data to defaults"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Reset user data to defaults
            cursor.execute('''
                UPDATE users 
                SET coins = 1000, personality_mode = 'friendly', total_commands = 0, last_daily = NULL
                WHERE user_id = ?
            ''', (user_id,))
            
            # Clear conversation history
            cursor.execute('''
                DELETE FROM conversations WHERE user_id = ?
            ''', (user_id,))
            
            # Clear usage data
            cursor.execute('''
                DELETE FROM usage WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"User data reset for {user_id}")
            
        except Exception as e:
            logger.error(f"Error resetting user data: {e}")
    
    def get_top_users(self, limit: int = 10) -> List[Dict]:
        """Get top users by coin balance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, coins, total_commands 
                FROM users 
                ORDER BY coins DESC 
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'user_id': row[0],
                    'coins': row[1],
                    'total_commands': row[2]
                }
                for row in results
            ]
            
        except Exception as e:
            logger.error(f"Error getting top users: {e}")
            return []

    def get_personality_mode(self, user_id: str) -> str:
        """Get user's personality mode, defaulting to 'friendly' if not set"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT personality_mode FROM users WHERE user_id = ?
            ''', (user_id,))
            result = cursor.fetchone()
            conn.close()
            if result and result[0]:
                return result[0]
            else:
                return 'friendly'
        except Exception as e:
            logger.error(f"Error getting personality mode: {e}")
            return 'friendly'
