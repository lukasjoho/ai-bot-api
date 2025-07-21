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

async def process_whatsapp_message(data: dict):
    phone_number, name, message_id, message_body, message_type = extract_whatsapp_data(data).values()
    
    if message_type != "text":
        response = "Ich kann nur Textnachrichten verstehen."
        data = create_text_message(phone_number, response)
        send_message(data)
        return
        
    response = await run_agent(message_body, message_id, phone_number, name)





