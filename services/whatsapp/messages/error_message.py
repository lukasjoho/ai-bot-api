"""Error message creation and sending functions"""

from services.whatsapp.api import send_message
from .text_message import create_text_message
from services.whatsapp.types import ErrorMessageData, TextMessageData

def create_error_message(phone_number: str, data: ErrorMessageData):
    # Default messages based on error type
    default_messages = {
        "ratelimit": "Wuff! 🐕 Mir qualmt gerade der Kopf - zu viele Fragen auf einmal! Gib mir kurz 1 Minute Pause und versuche es dann nochmal. Danke für dein Verständnis! 🐾",
        "exception": "Wuff! 🐕 Da ist wohl was schiefgelaufen... Kannst du deine Nachricht nochmal schicken? Ich bin gleich wieder da! 🐾"
    }
    
    # Use custom message or default
    message_text = data.custom_message or default_messages[data.message_type]
    text_data = TextMessageData(text=message_text)
    
    return create_text_message(phone_number, text_data)

def send_error_message(phone_number: str, data: ErrorMessageData):
    message_data = create_error_message(phone_number, data)
    send_message(message_data)

# Convenience functions for backward compatibility
def send_ratelimit_message(phone_number: str):
    data = ErrorMessageData(message_type="ratelimit")
    send_error_message(phone_number, data)

def send_exception_message(phone_number: str):
    data = ErrorMessageData(message_type="exception")
    send_error_message(phone_number, data)