from services.whatsapp.api import send_message
from .base import _create_base_message
from services.whatsapp.types import ReactionMessageData

def create_reaction_message(phone_number: str, data: ReactionMessageData):
    message = _create_base_message(phone_number, "reaction")
    message["reaction"] = {
        "message_id": data.message_id,
        "emoji": data.emoji
    }
    return message

def send_reaction_message(phone_number: str, data: ReactionMessageData):
    message_data = create_reaction_message(phone_number, data)
    send_message(message_data)