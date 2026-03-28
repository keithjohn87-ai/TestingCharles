"""
Email SendGrid Skill
Transactional emails, product delivery
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional


class EmailSendgrid:
    """Send transactional emails via SendGrid/SMTP."""
    
    def __init__(self, api_key: str = None, smtp_user: str = None, smtp_pass: str = None):
        self.api_key = api_key
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.smtp_server = "smtp.sendgrid.net"
        self.smtp_port = 587
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   from_email: str = "Charles@charles.ai") -> Dict:
        """Send a transactional email."""
        if not self.smtp_user or not self.smtp_pass:
            return {"error": "SMTP credentials not configured"}
        
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.smtp_user, self.smtp_pass)
                smtp.send_message(msg)
            return {"status": "sent", "to": to_email, "subject": subject}
        except Exception as e:
            return {"error": str(e)}
    
    def send_product(self, to_email: str, product_name: str, download_link: str) -> Dict:
        """Send product delivery email."""
        subject = f"Your Product: {product_name}"
        body = f"""
        <h2>Thank you for your purchase!</h2>
        <p>Your product <strong>{product_name}</strong> is ready.</p>
        <p>Download: <a href="{download_link}">{download_link}</a></p>
        <p>Best regards,<br>Charles</p>
        """
        return self.send_email(to_email, subject, body)
    
    def send_alert(self, to_email: str, alert_message: str, severity: str = "high") -> Dict:
        """Send alert email."""
        subject = f"[{severity.upper()}] Charles Alert"
        body = f"""
        <h2>⚠️ Alert</h2>
        <p>{alert_message}</p>
        """
        return self.send_email(to_email, subject, body)


SKILL_NAME = "email_sendgrid"
SKILL_DESCRIPTION = "Transactional emails, product delivery"
