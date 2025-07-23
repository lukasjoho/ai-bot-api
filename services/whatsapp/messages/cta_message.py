from services.whatsapp.messages import _create_base_message
from services.whatsapp.api import send_message
from services.whatsapp.types import CTAMessageData
from typing import Literal

def create_cta_message(phone_number: str, data: CTAMessageData):
    """
    Create a WhatsApp CTA (Call-to-Action) interactive message
    Args:
        phone_number: Recipient phone number
        data: CTA message data containing body_text, button_text, button_url, etc.
    """
    message = _create_base_message(phone_number, "interactive")
    message["interactive"] = {
        "type": "cta_url",
        "body": {
            "text": data.body_text
        },
        "action": {
            "name": "cta_url",
            "parameters": {
                "display_text": data.button_text,
                "url": data.button_url
            }
        }
    }
    
    # Add header if provided
    if data.header_type and data.header_content:
        if data.header_type == "text":
            message["interactive"]["header"] = {
                "type": "text",
                "text": data.header_content
            }
        elif data.header_type == "image":
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
    if data.footer_text:
        message["interactive"]["footer"] = {
            "text": data.footer_text
        }
    
    return message

def send_cta_message(phone_number: str, data: CTAMessageData):
    message_data = create_cta_message(phone_number, data)
    send_message(message_data)

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



