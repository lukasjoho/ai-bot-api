def _create_base_message(phone_number: str, message_type: str = None):
    """Create base message structure with common fields"""
    base = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
    }
    if message_type:
        base["type"] = message_type
    return base