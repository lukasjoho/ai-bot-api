from services.whatsapp.api import send_message
from services.whatsapp.types import TypingMessageData

def create_typing_indicator(data: TypingMessageData):
    message = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": data.message_id,
        "typing_indicator": {
            "type": "text"
        }
    }
    return message

def send_typing_indicator(data: TypingMessageData):
    message_data = create_typing_indicator(data)
    send_message(message_data)