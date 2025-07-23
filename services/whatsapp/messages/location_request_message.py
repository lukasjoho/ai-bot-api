from services.whatsapp.api import send_message
from services.whatsapp.messages import _create_base_message
from services.whatsapp.types import LocationRequestMessageData

def create_location_request_message(phone_number: str, data: LocationRequestMessageData):
    """
    Create a WhatsApp location request message that prompts the user to share their location
    Args:
        phone_number: Recipient phone number
        data: Location request message data containing body_text
    """
    message = _create_base_message(phone_number, "interactive")
    message["interactive"] = {
        "type": "location_request_message",
        "body": {
            "text": data.body_text
        },
        "action": {
            "name": "send_location"
        }
    }
    return message

def send_location_request_message(phone_number: str, data: LocationRequestMessageData):
    message_data = create_location_request_message(phone_number, data)
    send_message(message_data)