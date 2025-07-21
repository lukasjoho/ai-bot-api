import os
from dotenv import load_dotenv

load_dotenv()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

def verify_webhook(hub_mode: str | None, hub_verify_token: str | None, hub_challenge: str | None) -> str:
    print("Webhook verification started...")
    """Verify WhatsApp webhook subscription."""
    if not all([hub_mode, hub_verify_token, hub_challenge]):
        raise ValueError("Missing required verification parameters")
        
    if hub_mode != "subscribe" or hub_verify_token != VERIFY_TOKEN:
        raise ValueError("Invalid verification request")
        
    return hub_challenge