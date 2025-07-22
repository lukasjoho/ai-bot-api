import json
import logging
import asyncio
from services.whatsapp.utils import is_valid_whatsapp_message, extract_whatsapp_data
from services.openai.openai_agents import run_agent
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_text_message

def handle_message(data: dict):
    try:
        if is_valid_whatsapp_message(data):
            asyncio.create_task(process_whatsapp_message(data))
            return json.dumps({"message": "Valid WhatsApp message received", "status": "ok"}), 200
        else:
            logging.info("Not a WhatsApp API event")
            return json.dumps({"message": "Not a WhatsApp API event", "status": "error"}), 404

    except json.JSONDecodeError:
        logging.info("Invalid request body")
        return json.dumps({"message": "Invalid request body", "status": "error"}), 400

async def handleTextMessage(message: dict, phone_number: str, name: str, message_id: str):
    """Handle text messages by extracting body and invoking agent."""
    message_body = message["text"]["body"]
    await run_agent(message_body, message_id, phone_number, name)

async def handleLocationMessage(message: dict, phone_number: str, name: str, message_id: str):
    """Handle location messages by formatting location data and invoking agent."""
    location = message["location"]
    latitude = location["latitude"]
    longitude = location["longitude"]
    address = location.get("address", "")
    name_location = location.get("name", "")
    
    # Format location message for agent
    location_parts = []
    if name_location:
        location_parts.append(f"'{name_location}'")
    if address:
        location_parts.append(f"at {address}")
    location_parts.append(f"(Lat: {latitude}, Lng: {longitude})")
    
    location_message = f"User shared location: {' '.join(location_parts)}"
    await run_agent(location_message, message_id, phone_number, name)

async def handleInteractiveMessage(message: dict, phone_number: str, name: str, message_id: str):
    """Handle interactive messages (button clicks, list selections) by extracting selection and invoking agent."""
    interactive = message["interactive"]
    
    if "list_reply" in interactive:
        # User selected from a list
        selection_id = interactive["list_reply"]["id"]
        selection_title = interactive["list_reply"]["title"]
        interactive_message = f"User selected from list: '{selection_title}' (ID: {selection_id})"
    elif "button_reply" in interactive:
        # User clicked a button
        button_id = interactive["button_reply"]["id"] 
        button_title = interactive["button_reply"]["title"]
        interactive_message = f"User clicked button: '{button_title}' (ID: {button_id})"
    else:
        # Unknown interactive type
        interactive_message = "User interacted with message"
    
    await run_agent(interactive_message, message_id, phone_number, name)

async def process_whatsapp_message(data: dict):
    """Main message processor that routes to specific handlers."""
    extracted_data = extract_whatsapp_data(data)
    phone_number = extracted_data["phone_number"]
    name = extracted_data["name"] 
    message_id = extracted_data["message_id"]
    message_type = extracted_data["message_type"]
    message = extracted_data["message"]
    
    if not phone_number or not message_id or not message:
        logging.error("Invalid message data received")
        return
    
    # Route to specific message type handlers
    if message_type == "text":
        await handleTextMessage(message, phone_number, name, message_id)
    elif message_type == "location":
        await handleLocationMessage(message, phone_number, name, message_id)
    elif message_type == "interactive":
        await handleInteractiveMessage(message, phone_number, name, message_id)
    else:
        # Unsupported message type - send error response directly
        error_message = "Diese Nachricht kann ich nicht verarbeiten"
        response_data = create_text_message(phone_number, error_message)
        send_message(response_data)





