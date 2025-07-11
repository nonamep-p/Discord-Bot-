
import discord
import hashlib
import time
import logging
import json
import re
import asyncio
import io
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EnhancedSecurityManager:
    """Enterprise-grade security system for Discord bots"""
    
    def __init__(self):
        # Core security settings
        self.blocked_users: Set[str] = set()
        self.trusted_users: Set[str] = set()
        self.warned_users: Dict[str, List] = {}
        self.quarantined_users: Set[str] = set()
        
        # Auto moderation settings
        self.anti_spam_enabled = True
        self.bad_words_filter = True
        self.link_protection = True
        self.raid_protection = True
        self.nsfw_detection = True
        self.mass_mention_protection = True
        self.duplicate_message_protection = True
        
        # Content filtering
        self.profanity_level = 3  # 1-5 scale
        self.max_message_length = 2000
        self.max_mentions_per_message = 5
        self.max_emojis_per_message = 10
        self.image_scanning = True
        self.allowed_file_types = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.mov'}
        
        # Rate limiting
        self.message_rate_limit = 10  # messages per minute
        self.command_rate_limit = 5   # commands per minute
        self.reaction_rate_limit = 20 # reactions per minute
        
        # Raid protection
        self.join_rate_limit = 5      # users per minute
        self.auto_lockdown = True
        self.min_account_age = 7      # days
        self.auto_ban_new_accounts = False
        
        # Security logs
        self.security_logs: List[Dict] = []
        self.max_log_entries = 1000
        self.warnings_issued = 0
        
        # Blocked content
        self.blocked_words = {
            'tokens', 'discord_token', 'bot_token', 'api_key', 'secret', 'password',
            'invite_spammer', 'raid', 'nuke', 'crash', 'ddos', 'dox', 'doxx'
        }
        
        self.allowed_domains = {
            'discord.com', 'discord.gg', 'discordapp.com', 'youtube.com', 'youtu.be',
            'twitch.tv', 'twitter.com', 'github.com', 'reddit.com', 'imgur.com'
        }
        
        # Tracking
        self.user_activity: Dict[str, Dict] = {}
        self.suspicious_activity: Dict[str, List] = {}
        self.recent_joins: List[Dict] = []
        
    def log_security_event(self, event_type: str, description: str, user_id: str = None, 
                          severity: str = "medium", additional_data: Dict = None):
        """Log security events"""
        event = {
            'timestamp': time.time(),
            'type': event_type,
            'description': description,
            'user_id': user_id,
            'severity': severity,
            'additional_data': additional_data or {}
        }
        
        self.security_logs.append(event)
        
        # Keep only recent logs
        if len(self.security_logs) > self.max_log_entries:
            self.security_logs = self.security_logs[-self.max_log_entries:]
        
        logger.warning(f"Security Event [{severity.upper()}]: {event_type} - {description}")
        
    def check_comprehensive_security(self, message: discord.Message) -> tuple[bool, str, str]:
        """Comprehensive security check for messages"""
        user_id = str(message.author.id)
        content = message.content
        
        # Check if user is blocked
        if user_id in self.blocked_users:
            return False, "User is blocked", "blocked_user"
        
        # Skip checks for trusted users
        if user_id in self.trusted_users:
            return True, "Trusted user bypass", "trusted"
        
        # Anti-spam check
        if self.anti_spam_enabled and not self._check_spam(message):
            self.log_security_event("SPAM_DETECTED", f"Spam message from {message.author}", user_id, "high")
            return False, "Spam detected", "spam"
        
        # Bad words filter
        if self.bad_words_filter and not self._check_profanity(content):
            self.log_security_event("PROFANITY_DETECTED", f"Profanity from {message.author}", user_id, "medium")
            return False, "Inappropriate content", "profanity"
        
        # Link protection
        if self.link_protection and not self._check_links(content):
            self.log_security_event("SUSPICIOUS_LINK", f"Suspicious link from {message.author}", user_id, "high")
            return False, "Suspicious link detected", "suspicious_link"
        
        # Mass mention protection
        if self.mass_mention_protection and len(message.mentions) > self.max_mentions_per_message:
            self.log_security_event("MASS_MENTION", f"Mass mention from {message.author}", user_id, "high")
            return False, "Too many mentions", "mass_mention"
        
        # Message length check
        if len(content) > self.max_message_length:
            return False, "Message too long", "message_length"
        
        # NSFW content detection
        if self.nsfw_detection and self._check_nsfw_content(content):
            self.log_security_event("NSFW_CONTENT", f"NSFW content from {message.author}", user_id, "high")
            return False, "NSFW content detected", "nsfw"
        
        # Duplicate message check
        if self.duplicate_message_protection and self._check_duplicate_message(message):
            return False, "Duplicate message spam", "duplicate"
        
        return True, "Message approved", "approved"
    
    def _check_spam(self, message: discord.Message) -> bool:
        """Check for spam patterns"""
        user_id = str(message.author.id)
        current_time = time.time()
        
        if user_id not in self.user_activity:
            self.user_activity[user_id] = {'messages': [], 'commands': [], 'reactions': []}
        
        # Remove old messages (older than 1 minute)
        self.user_activity[user_id]['messages'] = [
            msg_time for msg_time in self.user_activity[user_id]['messages']
            if current_time - msg_time < 60
        ]
        
        # Check message rate
        if len(self.user_activity[user_id]['messages']) >= self.message_rate_limit:
            return False
        
        self.user_activity[user_id]['messages'].append(current_time)
        return True
    
    def _check_profanity(self, content: str) -> bool:
        """Check for inappropriate content based on profanity level"""
        content_lower = content.lower()
        
        # Basic profanity lists by level
        profanity_lists = {
            1: ['fuck', 'shit', 'damn'],  # Very lenient
            2: ['bitch', 'ass', 'crap'],  # Lenient
            3: ['retard', 'fag', 'gay'],  # Moderate
            4: ['nigger', 'cunt', 'whore'], # Strict
            5: ['kys', 'kill yourself', 'suicide'] # Very strict
        }
        
        for level in range(1, self.profanity_level + 1):
            for word in profanity_lists.get(level, []):
                if word in content_lower:
                    return False
        
        return True
    
    def _check_links(self, content: str) -> bool:
        """Check for suspicious links"""
        # Extract URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, content)
        
        for url in urls:
            domain = re.search(r'https?://([^/]+)', url)
            if domain:
                domain = domain.group(1).lower()
                # Check if domain is in whitelist
                if not any(allowed in domain for allowed in self.allowed_domains):
                    return False
        
        return True
    
    def _check_nsfw_content(self, content: str) -> bool:
        """Check for NSFW content"""
        nsfw_keywords = [
            'porn', 'xxx', 'sex', 'nude', 'naked', 'pussy', 'dick', 'cock',
            'nsfw', 'hentai', 'rule34', 'onlyfans', 'sexual'
        ]
        
        content_lower = content.lower()
        return not any(keyword in content_lower for keyword in nsfw_keywords)
    
    def _check_duplicate_message(self, message: discord.Message) -> bool:
        """Check for duplicate message spam"""
        user_id = str(message.author.id)
        content_hash = hashlib.md5(message.content.encode()).hexdigest()
        
        if user_id not in self.user_activity:
            self.user_activity[user_id] = {'message_hashes': []}
        
        recent_hashes = self.user_activity[user_id].get('message_hashes', [])
        
        # Check if same message sent recently
        if content_hash in recent_hashes[-5:]:  # Check last 5 messages
            return True
        
        recent_hashes.append(content_hash)
        if len(recent_hashes) > 10:
            recent_hashes = recent_hashes[-10:]
        
        self.user_activity[user_id]['message_hashes'] = recent_hashes
        return False
    
    def check_raid_protection(self, member: discord.Member) -> tuple[bool, str]:
        """Check for raid patterns"""
        if not self.raid_protection:
            return True, "Raid protection disabled"
        
        current_time = time.time()
        
        # Track recent joins
        self.recent_joins.append({
            'user_id': str(member.id),
            'timestamp': current_time,
            'account_age': (datetime.now() - member.created_at).days
        })
        
        # Remove old joins (older than 1 minute)
        self.recent_joins = [
            join for join in self.recent_joins
            if current_time - join['timestamp'] < 60
        ]
        
        # Check join rate
        if len(self.recent_joins) > self.join_rate_limit:
            self.log_security_event("RAID_DETECTED", f"High join rate detected: {len(self.recent_joins)} joins", 
                                   severity="critical")
            return False, "Raid detected - high join rate"
        
        # Check account age
        account_age = (datetime.now() - member.created_at).days
        if account_age < self.min_account_age:
            self.log_security_event("SUSPICIOUS_ACCOUNT", f"New account joined: {member} (age: {account_age} days)", 
                                   str(member.id), "medium")
            
            if self.auto_ban_new_accounts:
                return False, f"Account too new ({account_age} days)"
        
        return True, "Join approved"
    
    def block_user(self, user_id: str, reason: str, moderator_id: str = None):
        """Block a user"""
        self.blocked_users.add(user_id)
        self.log_security_event("USER_BLOCKED", f"User {user_id} blocked: {reason}", user_id, "high",
                               {'moderator_id': moderator_id})
    
    def unblock_user(self, user_id: str):
        """Unblock a user"""
        self.blocked_users.discard(user_id)
        self.log_security_event("USER_UNBLOCKED", f"User {user_id} unblocked", user_id, "medium")
    
    def add_trusted_user(self, user_id: str):
        """Add user to trusted list"""
        self.trusted_users.add(user_id)
        self.log_security_event("USER_TRUSTED", f"User {user_id} added to trusted list", user_id, "low")
    
    def remove_trusted_user(self, user_id: str):
        """Remove user from trusted list"""
        self.trusted_users.discard(user_id)
        self.log_security_event("USER_UNTRUSTED", f"User {user_id} removed from trusted list", user_id, "low")
    
    def warn_user(self, user_id: str, reason: str, moderator_id: str = None):
        """Issue warning to user"""
        if user_id not in self.warned_users:
            self.warned_users[user_id] = []
        
        warning = {
            'timestamp': time.time(),
            'reason': reason,
            'moderator_id': moderator_id
        }
        
        self.warned_users[user_id].append(warning)
        self.warnings_issued += 1
        
        self.log_security_event("USER_WARNING", f"Warning issued to {user_id}: {reason}", user_id, "medium",
                               {'moderator_id': moderator_id})
    
    def get_user_warnings(self, user_id: str) -> List[Dict]:
        """Get user warnings"""
        return self.warned_users.get(user_id, [])
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent security logs"""
        return self.security_logs[-limit:] if self.security_logs else []
    
    def get_all_logs(self) -> List[Dict]:
        """Get all security logs"""
        return self.security_logs
    
    def clear_logs(self):
        """Clear all security logs"""
        self.security_logs.clear()
        self.log_security_event("LOGS_CLEARED", "Security logs cleared", severity="low")
    
    def export_security_data(self) -> Dict:
        """Export all security data"""
        return {
            'blocked_users': list(self.blocked_users),
            'trusted_users': list(self.trusted_users),
            'warned_users': self.warned_users,
            'security_logs': self.security_logs,
            'settings': {
                'anti_spam_enabled': self.anti_spam_enabled,
                'bad_words_filter': self.bad_words_filter,
                'link_protection': self.link_protection,
                'raid_protection': self.raid_protection,
                'nsfw_detection': self.nsfw_detection,
                'profanity_level': self.profanity_level,
                'join_rate_limit': self.join_rate_limit,
                'auto_lockdown': self.auto_lockdown
            }
        }
    
    def import_security_data(self, data: Dict):
        """Import security data"""
        if 'blocked_users' in data:
            self.blocked_users = set(data['blocked_users'])
        if 'trusted_users' in data:
            self.trusted_users = set(data['trusted_users'])
        if 'warned_users' in data:
            self.warned_users = data['warned_users']
        if 'security_logs' in data:
            self.security_logs = data['security_logs']
        if 'settings' in data:
            settings = data['settings']
            for key, value in settings.items():
                if hasattr(self, key):
                    setattr(self, key, value)
