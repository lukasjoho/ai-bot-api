"""Image message creation and sending functions"""

from services.whatsapp.utils import process_text_for_whatsapp
from services.whatsapp.api import send_message
from .base import _create_base_message
from services.whatsapp.types import ImageMessageData

def create_image_message(phone_number: str, data: ImageMessageData):
    caption = process_text_for_whatsapp(data.caption or "")
    message = _create_base_message(phone_number, "image")
    message["image"] = {
        "link": data.image_url,
        "caption": caption
    }
    return message

def send_image_message(phone_number: str, data: ImageMessageData):
    message_data = create_image_message(phone_number, data)
    send_message(message_data)