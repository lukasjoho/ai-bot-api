from typing import Any, Union

from services.whatsapp.messages import (
    send_text_message, 
    send_image_message, 
    send_location_message,
)
from services.whatsapp.types import (
    ImageMessage,
    TextMessage,
    LocationMessage,
)



def dispatch_message(phone_number: str, message: Union[TextMessage, ImageMessage, LocationMessage]) -> bool:
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
        
        else:
            print(f"Unsupported message type: {message.type}")
            return False
        
    except Exception as e:
        print(f"Failed to dispatch message: {e}")
        return False