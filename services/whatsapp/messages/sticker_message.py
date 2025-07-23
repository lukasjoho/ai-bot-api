from services.whatsapp.api import send_message
from services.whatsapp.messages import _create_base_message
from services.whatsapp.types import StickerMessageData

def create_sticker_message(phone_number: str, data: StickerMessageData):
    """
    Create a WhatsApp sticker message
    Args:
        phone_number: Recipient phone number
        data: Sticker message data containing sticker_id or sticker_url
    """
    message = _create_base_message(phone_number, "sticker")
    
    if data.sticker_url:
        message["sticker"] = {"link": data.sticker_url}
    else:
        raise ValueError("Either sticker_id or sticker_url must be provided")
    
    return message

def send_sticker_message(phone_number: str, data: StickerMessageData):
    message_data = create_sticker_message(phone_number, data)
    send_message(message_data)