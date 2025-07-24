from typing import Any, Union

from services.whatsapp.messages import (
    send_text_message, 
    send_image_message, 
    send_location_message,
    send_cta_message,
    send_location_request_message,
    send_interactive_list_message,
    send_sticker_message,
)
from services.whatsapp.types import (
    ImageMessage,
    TextMessage,
    LocationMessage,
    CTAMessage,
    LocationRequestMessage,
    InteractiveListMessage,
    StickerMessage,
)



def dispatch_message(phone_number: str, message: Union[TextMessage, ImageMessage, LocationMessage, CTAMessage, LocationRequestMessage, InteractiveListMessage, StickerMessage]) -> bool:
    try:
        if message.type == "text":
            send_text_message(phone_number, message.data)
            return True     
        elif message.type == "image":
            send_image_message(phone_number, message.data)
            return True 
        elif message.type == "location":
            send_location_message(phone_number, message.data)
            return True
        elif message.type == "cta":
            send_cta_message(phone_number, message.data)
            return True
        elif message.type == "location_request":
            send_location_request_message(phone_number, message.data)
            return True
        elif message.type == "interactive_list":
            send_interactive_list_message(phone_number, message.data)
            return True
        elif message.type == "sticker":
            send_sticker_message(phone_number, message.data)
            return True
        else:
            print(f"Unsupported message type: {message.type}")
            return False
        
    except Exception as e:
        print(f"Failed to dispatch message: {e}")
        return False