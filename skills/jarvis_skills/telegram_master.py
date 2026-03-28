"""
Telegram Master Skill
Full bot management, broadcast, automation
"""

import requests
from typing import Dict, Any, List, Optional


class TelegramMaster:
    """Manage Telegram bot operations."""
    
    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token
        self.api_base = f"https://api.telegram.org/bot{bot_token}" if bot_token else None
    
    def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> Dict:
        """Send a message via Telegram bot."""
        if not self.api_base:
            return {"error": "No bot token configured"}
        
        url = f"{self.api_base}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
        
        try:
            resp = requests.post(url, json=data, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    def broadcast(self, chat_ids: List[str], message: str) -> Dict:
        """Broadcast message to multiple chat IDs."""
        results = []
        for cid in chat_ids:
            result = self.send_message(cid, message)
            results.append({"chat_id": cid, "result": result})
        return {"broadcasted": len(results), "results": results}
    
    def get_updates(self, offset: int = None, limit: int = 100) -> Dict:
        """Get bot updates."""
        if not self.api_base:
            return {"error": "No bot token configured"}
        
        url = f"{self.api_base}/getUpdates"
        params = {"limit": limit}
        if offset:
            params["offset"] = offset
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    def set_webhook(self, webhook_url: str) -> Dict:
        """Set webhook URL."""
        if not self.api_base:
            return {"error": "No bot token configured"}
        
        url = f"{self.api_base}/setWebhook"
        data = {"url": webhook_url}
        
        try:
            resp = requests.post(url, json=data, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_me(self) -> Dict:
        """Get bot information."""
        if not self.api_base:
            return {"error": "No bot token configured"}
        
        url = f"{self.api_base}/getMe"
        
        try:
            resp = requests.get(url, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}


SKILL_NAME = "telegram_master"
SKILL_DESCRIPTION = "Full bot management, broadcast, automation"
