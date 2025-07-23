from services.whatsapp.utils import process_text_for_whatsapp
from services.whatsapp.api import send_message
from .base import _create_base_message
from services.whatsapp.types import TextMessageData

def create_text_message(phone_number: str, data: TextMessageData):
    text = process_text_for_whatsapp(data.text)
    message = _create_base_message(phone_number, "text")
    message["text"] = {"body": text}
    return message

def send_text_message(phone_number: str, data: TextMessageData):
    message_data = create_text_message(phone_number, data)
    send_message(message_data)