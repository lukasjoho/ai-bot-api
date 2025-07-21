from services.whatsapp.utils import process_text_for_whatsapp

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

def create_text_message(phone_number: str, text: str):
    text = process_text_for_whatsapp(text)
    message = _create_base_message(phone_number, "text")
    message["text"] = {"body": text}
    return message

def create_image_message(phone_number: str, image_url: str, caption: str = ""):
    caption = process_text_for_whatsapp(caption)
    message = _create_base_message(phone_number, "image")
    message["image"] = {
        "link": image_url,
        "caption": caption
    }
    return message

def create_reaction_message(phone_number: str, message_id: str, emoji: str):
    message = _create_base_message(phone_number, "reaction")
    message["reaction"] = {
        "message_id": message_id,
        "emoji": emoji
    }
    return message

def create_location_message(phone_number: str, latitude: float, longitude: float, name: str, address: str):
    message = _create_base_message(phone_number, "location")
    message["location"] = {
        "latitude": latitude,
        "longitude": longitude,
        "name": name,
        "address": address
    }
    return message

def create_read_notification(message_id: str):
    return {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }

def create_typing_indicator(message_id: str):
    return {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
        "typing_indicator": {
            "type": "text"
        }
    }

def create_cta_message(phone_number: str, body_text: str, button_text: str, button_url: str, header_type: str = None, header_content: str = None, footer_text: str = None):
    """
    Create a WhatsApp CTA (Call-to-Action) interactive message
    Args:
        phone_number: Recipient phone number
        body_text: Main message text
        button_text: Text displayed on the button
        button_url: URL the button links to
        header_type: Optional header type ("text", "image", "video", "document")
        header_content: Header content (text or URL)
        footer_text: Optional footer text
    """
    message = _create_base_message(phone_number, "interactive")
    message["interactive"] = {
        "type": "cta_url",
        "body": {
            "text": body_text
        },
        "action": {
            "name": "cta_url",
            "parameters": {
                "display_text": button_text,
                "url": button_url
            }
        }
    }
    
    # Add header if provided
    if header_type and header_content:
        if header_type == "text":
            message["interactive"]["header"] = {
                "type": "text",
                "text": header_content
            }
        elif header_type in ["image", "video", "document"]:
            message["interactive"]["header"] = {
                "type": header_type,
                header_type: {
                    "link": header_content
                }
            }
    
    # Add footer if provided
    if footer_text:
        message["interactive"]["footer"] = {
            "text": footer_text
        }
    
    return message