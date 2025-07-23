from services.whatsapp.messages import _create_base_message
from services.whatsapp.api import send_message
from services.whatsapp.types import InteractiveListMessageData

def create_interactive_list_message(phone_number: str, data: InteractiveListMessageData):
    """
    Create a WhatsApp interactive list message
    Args:
        phone_number: Recipient phone number
        data: Interactive list message data containing body_text, button_text, and sections
    """
    message = _create_base_message(phone_number, "interactive")
    
    # Validate and clean sections - ensure titles and descriptions are within limits
    cleaned_sections = []
    for section in data.sections:
        cleaned_rows = []
        for row in section.rows:
            # WhatsApp has character limits: title max 24 chars, description max 72 chars
            cleaned_row = {
                "id": str(row.id),  # Ensure ID is string
                "title": str(row.title)[:24],  # Truncate if too long
                "description": str(row.description or "")[:72]  # Truncate if too long
            }
            cleaned_rows.append(cleaned_row)
        
        if cleaned_rows:  # Only add section if it has rows
            cleaned_sections.append({
                "title": str(section.title)[:24],  # Section title also has limits
                "rows": cleaned_rows
            })
    
    message["interactive"] = {
        "type": "list",
        "body": {
            "text": data.body_text
        },
        "action": {
            "button": data.button_text,
            "sections": cleaned_sections
        }
    }
    return message

def send_interactive_list_message(phone_number: str, data: InteractiveListMessageData):
    message_data = create_interactive_list_message(phone_number, data)
    send_message(message_data)