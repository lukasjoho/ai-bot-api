import requests
import json
import logging
import os
import asyncio
from services.whatsapp.utils import is_valid_whatsapp_message, process_text_for_whatsapp
from services.whatsapp.respond import generate_response

from services.openai.openai import generate_openai_response

from dotenv import load_dotenv


load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
VERSION = os.getenv("WHATSAPP_API_VERSION")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
RECIPIENT_WAID = os.getenv("WHATSAPP_RECIPIENT_DEMO_WAID")

def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template":{"name": "hello_world", "language": {"code":"en_US"}}
    }
    response = requests.post(url, headers=headers, json=data)
    return response

def send_message(data: dict):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        logging.info("Message sent successfully")
    except requests.Timeout:
        logging.error("Request timed out")
        return json.dumps({"message": "Request timed out", "status": "error"}), 408
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message: {e}")
        return json.dumps({"message": "Failed to send message", "status": "error"}), 500
    return response


    
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
    wa_id = data["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = data["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
    message = data["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]
    print(f"Contact: {name} {wa_id}")
    if message.get("type") != "text":
        response = "Ich kann nur Textnachrichten verstehen."
        data = create_response_message(wa_id, response)
        send_message(data)
        return

    # respond with text to uppercase all
    # response = generate_response(message_body, wa_id)
    response = await generate_openai_response(message_body, wa_id)
    response = process_text_for_whatsapp(response)
    data = create_response_message(wa_id, response)
    send_message(data)

def create_response_message(recipient: str, response: str):
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {"body": response}
    }



