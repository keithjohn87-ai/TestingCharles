"""
Product Delivery Skill
Automated file delivery on purchase
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, List


class ProductDelivery:
    """Deliver products automatically on purchase."""
    
    def __init__(self, delivery_folder: str = "/opt/charles/products"):
        self.delivery_folder = delivery_folder
    
    def deliver(self, customer_email: str, product_file: str) -> Dict:
        """Deliver product file to customer."""
        file_path = os.path.join(self.delivery_folder, product_file)
        
        if not os.path.exists(file_path):
            return {"error": f"Product file not found: {product_file}"}
        
        return {
            "action": "deliver",
            "file": product_file,
            "to": customer_email,
            "status": "ready"
        }
    
    def deliver_link(self, customer_email: str, product_name: str, download_link: str) -> Dict:
        """Send download link to customer."""
        subject = f"Your Download: {product_name}"
        body = f"""
        <h2>Thank you for your purchase!</h2>
        <p>Download: <a href="{download_link}">{download_link}</a></p>
        """
        
        return {
            "action": "deliver_link",
            "product": product_name,
            "to": customer_email,
            "status": "ready"
        }
    
    def verify_delivery(self, product_name: str) -> Dict:
        """Verify product is available for delivery."""
        file_path = os.path.join(self.delivery_folder, product_name)
        
        return {
            "product": product_name,
            "available": os.path.exists(file_path)
        }


SKILL_NAME = "product_delivery"
SKILL_DESCRIPTION = "Automated file delivery on purchase"
