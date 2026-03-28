"""
SMS Twilio Skill
SMS alerts for critical issues
"""

from twilio.rest import Client
from typing import Dict, Any, List


class SmsTwilio:
    """Send SMS via Twilio."""
    
    def __init__(self, account_sid: str = None, auth_token: str = None, from_number: str = None):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.client = None
        
        if account_sid and auth_token:
            self.client = Client(account_sid, auth_token)
    
    def send_sms(self, to_number: str, message: str) -> Dict:
        """Send SMS message."""
        if not self.client:
            return {"error": "Twilio not configured"}
        
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return {"status": "sent", "sid": msg.sid}
        except Exception as e:
            return {"error": str(e)}
    
    def send_alert(self, to_number: str, alert: str) -> Dict:
        """Send critical alert."""
        return self.send_sms(to_number, f"Charles Alert: {alert}")


SKILL_NAME = "sms_twilio"
SKILL_DESCRIPTION = "SMS alerts for critical issues"
