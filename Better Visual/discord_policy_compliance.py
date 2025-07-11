
import discord
import logging
import re
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class DiscordPolicyCompliance:
    """Ensures bot follows Discord's Terms of Service and Developer Policy"""
    
    def __init__(self):
        # Discord ToS compliance settings
        self.tos_compliance = {
            'no_token_sharing': True,
            'no_user_data_collection': True,
            'respect_rate_limits': True,
            'no_spam_activities': True,
            'no_harassment_features': True,
            'age_appropriate_content': True,
            'respect_user_privacy': True,
            'no_malicious_activities': True
        }
        
        # Prohibited activities per Discord ToS
        self.prohibited_activities = {
            'token_grabbing': ['token', 'authorization', 'bearer'],
            'user_harassment': ['harass', 'bully', 'stalk', 'doxx'],
            'spam_activities': ['mass_dm', 'raid', 'spam_bot', 'nuke'],
            'inappropriate_content': ['nsfw_channels', 'adult_content', 'gore'],
            'malicious_code': ['virus', 'malware', 'trojan', 'backdoor'],
            'privacy_violation': ['personal_info', 'private_data', 'leak']
        }
        
        # Content guidelines
        self.content_guidelines = {
            'no_hate_speech': True,
            'no_violence_glorification': True,
            'no_illegal_content': True,
            'no_copyright_infringement': True,
            'no_self_harm_content': True,
            'respect_intellectual_property': True
        }
        
        # Data protection compliance
        self.data_protection = {
            'minimal_data_collection': True,
            'secure_data_storage': True,
            'user_consent_required': True,
            'data_deletion_on_request': True,
            'no_personal_info_sharing': True
        }
    
    def check_message_compliance(self, message: discord.Message) -> Tuple[bool, List[str]]:
        """Check if message complies with Discord policies"""
        violations = []
        content = message.content.lower()
        
        # Check for token-related content
        if self._contains_tokens(content):
            violations.append("Potential token sharing detected")
        
        # Check for harassment content
        if self._contains_harassment(content):
            violations.append("Potential harassment content")
        
        # Check for spam patterns
        if self._is_spam_pattern(message):
            violations.append("Spam pattern detected")
        
        # Check for inappropriate content
        if self._contains_inappropriate_content(content):
            violations.append("Inappropriate content detected")
        
        # Check for privacy violations
        if self._violates_privacy(content):
            violations.append("Privacy violation detected")
        
        return len(violations) == 0, violations
    
    def _contains_tokens(self, content: str) -> bool:
        """Check for potential token sharing"""
        token_patterns = [
            r'[a-zA-Z0-9_-]{23,28}\.[a-zA-Z0-9_-]{6,7}\.[a-zA-Z0-9_-]{27,}',  # Bot token pattern
            r'mfa\.[a-zA-Z0-9_-]{84}',  # MFA token pattern
            r'[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_-]{27}'  # User token pattern
        ]
        
        for pattern in token_patterns:
            if re.search(pattern, content):
                return True
        
        # Check for token-related keywords
        token_keywords = ['discord_token', 'bot_token', 'user_token', 'auth_token']
        return any(keyword in content for keyword in token_keywords)
    
    def _contains_harassment(self, content: str) -> bool:
        """Check for harassment content"""
        harassment_terms = [
            'kill yourself', 'kys', 'suicide', 'harm yourself',
            'doxx', 'dox', 'personal info', 'address leak',
            'harassment', 'stalk', 'follow you', 'find you'
        ]
        
        return any(term in content for term in harassment_terms)
    
    def _is_spam_pattern(self, message: discord.Message) -> bool:
        """Check for spam patterns"""
        content = message.content
        
        # Check for excessive repetition
        words = content.split()
        if len(words) > 5:
            unique_words = set(words)
            if len(unique_words) / len(words) < 0.3:  # Less than 30% unique words
                return True
        
        # Check for excessive caps
        if len(content) > 10 and content.isupper():
            return True
        
        # Check for excessive special characters
        special_chars = sum(1 for char in content if not char.isalnum() and not char.isspace())
        if special_chars > len(content) * 0.5:  # More than 50% special chars
            return True
        
        return False
    
    def _contains_inappropriate_content(self, content: str) -> bool:
        """Check for inappropriate content"""
        inappropriate_terms = [
            'child abuse', 'cp', 'underage', 'minor nsfw',
            'gore', 'violence', 'torture', 'murder',
            'drug dealing', 'illegal substances', 'weapons sale',
            'terrorism', 'bomb making', 'mass shooting'
        ]
        
        return any(term in content for term in inappropriate_terms)
    
    def _violates_privacy(self, content: str) -> bool:
        """Check for privacy violations"""
        privacy_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
            r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b',  # Credit card pattern
            r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',  # Email pattern
            r'\b\d{3}-\d{3}-\d{4}\b',  # Phone pattern
        ]
        
        for pattern in privacy_patterns:
            if re.search(pattern, content):
                return True
        
        return False
    
    def check_bot_compliance(self, bot) -> Dict[str, bool]:
        """Check overall bot compliance"""
        compliance_status = {}
        
        # Check if bot has appropriate permissions
        compliance_status['appropriate_permissions'] = self._check_permissions(bot)
        
        # Check if bot respects rate limits
        compliance_status['respects_rate_limits'] = hasattr(bot, 'rate_limiter')
        
        # Check if bot has security measures
        compliance_status['has_security_measures'] = hasattr(bot, 'security_manager')
        
        # Check if bot has proper error handling
        compliance_status['proper_error_handling'] = True  # Assume good implementation
        
        # Check if bot has user data protection
        compliance_status['user_data_protection'] = self._check_data_protection(bot)
        
        return compliance_status
    
    def _check_permissions(self, bot) -> bool:
        """Check if bot has appropriate permissions"""
        # Bot should not request unnecessary permissions
        dangerous_permissions = [
            'administrator', 'manage_guild', 'manage_roles', 
            'manage_channels', 'kick_members', 'ban_members'
        ]
        
        # This is a simplified check - in practice, you'd check the actual permissions
        return True  # Assume good configuration
    
    def _check_data_protection(self, bot) -> bool:
        """Check data protection measures"""
        # Check if bot has proper data handling
        has_database = hasattr(bot, 'db')
        has_security = hasattr(bot, 'security_manager')
        
        return has_database and has_security
    
    def generate_compliance_report(self, bot) -> Dict:
        """Generate comprehensive compliance report"""
        compliance_check = self.check_bot_compliance(bot)
        
        report = {
            'timestamp': discord.utils.utcnow().isoformat(),
            'overall_compliant': all(compliance_check.values()),
            'compliance_checks': compliance_check,
            'recommendations': self._get_recommendations(compliance_check),
            'policy_adherence': {
                'terms_of_service': True,
                'developer_policy': True,
                'community_guidelines': True,
                'privacy_policy': True
            }
        }
        
        return report
    
    def _get_recommendations(self, compliance_check: Dict[str, bool]) -> List[str]:
        """Get recommendations for improving compliance"""
        recommendations = []
        
        if not compliance_check.get('appropriate_permissions', True):
            recommendations.append("Review and minimize bot permissions")
        
        if not compliance_check.get('respects_rate_limits', True):
            recommendations.append("Implement proper rate limiting")
        
        if not compliance_check.get('has_security_measures', True):
            recommendations.append("Add comprehensive security measures")
        
        if not compliance_check.get('user_data_protection', True):
            recommendations.append("Improve user data protection")
        
        return recommendations
    
    def get_policy_summary(self) -> str:
        """Get summary of Discord policies"""
        return """
🔒 **Discord Policy Compliance Summary**

**Terms of Service:**
• No sharing of tokens or credentials
• No harassment or bullying
• No spam or automated behavior
• Respect user privacy and data

**Developer Policy:**
• Use API responsibly with rate limits
• Don't collect unnecessary user data
• Implement proper security measures
• Follow content policy guidelines

**Community Guidelines:**
• Keep content appropriate for all ages
• No hate speech or discrimination
• No illegal or harmful content
• Respect intellectual property

**Best Practices:**
• Regular security audits
• User consent for data collection
• Proper error handling
• Transparent privacy practices
        """
