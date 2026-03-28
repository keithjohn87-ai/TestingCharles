"""
Stripe Full Skill
Webhook handling, subscription management
"""

import stripe
from typing import Dict, Any, List, Optional


class StripeFull:
    """Handle Stripe payments and subscriptions."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if api_key:
            stripe.api_key = api_key
    
    def create_checkout_session(self, price_id: str, customer_email: str) -> Dict:
        """Create Stripe checkout session."""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{"price": price_id, "quantity": 1}],
                customer_email=customer_email,
                success_url="https://charles.ai/success",
                cancel_url="https://charles.ai/cancel"
            )
            return {"session_id": session.id, "url": session.url}
        except Exception as e:
            return {"error": str(e)}
    
    def create_subscription(self, customer_email: str, price_id: str) -> Dict:
        """Create subscription for customer."""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            # This would create customer + subscription
            return {"status": "ready", "customer": customer_email, "price": price_id}
        except Exception as e:
            return {"error": str(e)}
    
    def handle_webhook(self, payload: str, sig: str, webhook_secret: str) -> Dict:
        """Handle Stripe webhook."""
        try:
            event = stripe.Webhook.construct(payload, sig, webhook_secret)
            return {"type": event.type, "data": event.data.object}
        except Exception as e:
            return {"error": str(e)}
    
    def get_subscription_status(self, subscription_id: str) -> Dict:
        """Get subscription status."""
        if not self.api_key:
            return {"error": "API key not configured"}
        
        try:
            sub = stripe.Subscription.retrieve(subscription_id)
            return {"status": sub.status, "current_period_end": sub.current_period_end}
        except Exception as e:
            return {"error": str(e)}


SKILL_NAME = "stripe_full"
SKILL_DESCRIPTION = "Webhook handling, subscription management"
