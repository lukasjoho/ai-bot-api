from services.whatsapp.messages import _create_base_message
from services.whatsapp.api import send_message
from services.whatsapp.types import InteractiveListMessageData

def create_interactive_list_message(phone_number: str, data: InteractiveListMessageData):
    message = _create_base_message(phone_number, "interactive")
    
    items = []
    for item in data.items:
        item = {
            "id": str(len(items) + 1),
            "title": str(item.title)[:24],
            "description": str(item.description)[:72]
        }
        items.append(item)
    
    # Create a single section with all items
    section = {
        "title": "Optionen",  # Section title also has limits
        "rows": items
    }
    
    message["interactive"] = {
        "type": "list",
        "header": {
            "type": "text",
            "text": data.header_text
        },
        "body": {
            "text": data.body_text
        },
        "action": {
            "button": data.button_text,
            "sections": [section]  # Single section containing all items
        }
    }
    return message

def send_interactive_list_message(phone_number: str, data: InteractiveListMessageData):
    message_data = create_interactive_list_message(phone_number, data)
    send_message(message_data)