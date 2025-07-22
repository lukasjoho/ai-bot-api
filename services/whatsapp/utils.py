import re

def is_valid_whatsapp_message(data: dict) -> bool:
    try:
        return (
            data.get("entry", [{}])[0]
            .get("changes", [{}])[0]
            .get("value", {})
            .get("messages", []) != []
        )
    except (IndexError, KeyError):
        return False
    
def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text

def extract_whatsapp_data(data: dict) -> dict:
    """Extract core WhatsApp data and message object for further processing."""
    try:
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        contact = value["contacts"][0]
        message = value["messages"][0]
        
        return {
            "phone_number": contact["wa_id"],
            "name": contact["profile"]["name"],
            "message_id": message["id"],
            "message_type": message.get("type", "text"),
            "message": message  # Raw message object for type-specific handlers
        }
    except (KeyError, IndexError, TypeError):
        return {
            "phone_number": None,
            "name": None,
            "message_id": None,
            "message_type": None,
            "message": None
        }

