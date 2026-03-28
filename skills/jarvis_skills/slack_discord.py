"""
Slack Discord Bridge Skill
Multi-platform presence
"""

import requests
from typing import Dict, Any


class SlackDiscord:
    """Bridge messages between Slack and Discord."""
    
    def __init__(self, slack_webhook: str = None, discord_webhook: str = None):
        self.slack_webhook = slack_webhook
        self.discord_webhook = discord_webhook
    
    def send_slack(self, message: str, channel: str = None) -> Dict:
        """Send message to Slack."""
        if not self.slack_webhook:
            return {"error": "Slack webhook not configured"}
        
        try:
            resp = requests.post(self.slack_webhook, json={"text": message}, timeout=10)
            return {"status": "sent", "platform": "slack"}
        except Exception as e:
            return {"error": str(e)}
    
    def send_discord(self, message: str) -> Dict:
        """Send message to Discord."""
        if not self.discord_webhook:
            return {"error": "Discord webhook not configured"}
        
        try:
            resp = requests.post(self.discord_webhook, json={"content": message}, timeout=10)
            return {"status": "sent", "platform": "discord"}
        except Exception as e:
            return {"error": str(e)}
    
    def broadcast(self, message: str) -> Dict:
        """Broadcast to both platforms."""
        results = []
        
        if self.slack_webhook:
            results.append(self.send_slack(message))
        
        if self.discord_webhook:
            results.append(self.send_discord(message))
        
        return {"broadcasted": len(results), "results": results}


SKILL_NAME = "slack_discord"
SKILL_DESCRIPTION = "Multi-platform presence"
