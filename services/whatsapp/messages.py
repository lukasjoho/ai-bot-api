from typing import Literal
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

def create_cta_message(phone_number: str, body_text: str, button_text: str, button_url: str, header_type: Literal["text", "image"] = None, header_content: str = None, footer_text: str = None):
    """
    Create a WhatsApp CTA (Call-to-Action) interactive message
    Args:
        phone_number: Recipient phone number
        body_text: Main message text
        button_text: Text displayed on the button
        button_url: URL the button links to
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
        elif header_type == "image":
            OG_IMAGE = "https://d23dsm0lnesl7r.cloudfront.net/media/91/3f/77/1713433379/bb-open-graph-image-BELCANDO.jpeg"
            imageUrl = OG_IMAGE
            # Validate image URL
            if _is_valid_image_url(imageUrl):
                message["interactive"]["header"] = {
                    "type": "image",
                    "image": {
                        "link": imageUrl
                    }
                }
    
    # Add footer if provided
    if footer_text:
        message["interactive"]["footer"] = {
            "text": footer_text
        }
    
    return message

def _is_valid_image_url(url: str) -> bool:
    """Validate if URL is a valid image URL"""
    if not url:
        return False
        
    # Check for invalid/example URLs
    invalid_patterns = ["example.com", "placeholder", "dummy", "test", "lorem", "temp"]
    if any(pattern in url.lower() for pattern in invalid_patterns):
        return False
    
    # Check if URL has image extension
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
    if not any(url.lower().endswith(ext) for ext in image_extensions):
        return False
    
    try:
        import requests
        # Quick HEAD request to validate URL exists and is an image
        response = requests.head(url, timeout=5)
        if response.status_code >= 400:
            return False
            
        # Check content-type header
        content_type = response.headers.get('content-type', '').lower()
        if content_type and 'image/' in content_type:
            return True
            
        # Fallback: if no content-type header, trust the file extension
        return any(url.lower().endswith(ext) for ext in image_extensions)
        
    except Exception:
        # If validation fails, reject the URL
        return False

def create_location_request_message(phone_number: str, body_text: str):
    """
    Create a WhatsApp location request message that prompts the user to share their location
    Args:
        phone_number: Recipient phone number
        body_text: Text asking for location (e.g., "Please share your location")
    """
    message = _create_base_message(phone_number, "interactive")
    message["interactive"] = {
        "type": "location_request_message",
        "body": {
            "text": body_text
        },
        "action": {
            "name": "send_location"
        }
    }
    return message

def create_interactive_list_message(phone_number: str, body_text: str, button_text: str, sections: list):
    """
    Create a WhatsApp interactive list message
    Args:
        phone_number: Recipient phone number
        body_text: Main message text
        button_text: Text on the button to open the list (e.g., "Auswählen")
        sections: List of sections, each containing rows with id, title, and description
                 Format: [{"title": "Section Title", "rows": [{"id": "item_id", "title": "Item Title", "description": "Item Description"}]}]
    """
    message = _create_base_message(phone_number, "interactive")
    
    # Validate and clean sections - ensure titles and descriptions are within limits
    cleaned_sections = []
    for section in sections:
        cleaned_rows = []
        for row in section.get("rows", []):
            # WhatsApp has character limits: title max 24 chars, description max 72 chars
            cleaned_row = {
                "id": str(row["id"]),  # Ensure ID is string
                "title": str(row["title"])[:24],  # Truncate if too long
                "description": str(row.get("description", ""))[:72]  # Truncate if too long
            }
            cleaned_rows.append(cleaned_row)
        
        if cleaned_rows:  # Only add section if it has rows
            cleaned_sections.append({
                "title": str(section["title"])[:24],  # Section title also has limits
                "rows": cleaned_rows
            })
    
    message["interactive"] = {
        "type": "list",
        "body": {
            "text": body_text
        },
        "action": {
            "button": button_text,
            "sections": cleaned_sections
        }
    }
    return message