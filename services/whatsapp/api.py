import os
import requests
import logging
import json
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
VERSION = os.getenv("WHATSAPP_API_VERSION") 
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

# Validate required environment variables
if not ACCESS_TOKEN:
    raise ValueError("WHATSAPP_ACCESS_TOKEN environment variable is required")
if not VERSION:
    raise ValueError("WHATSAPP_API_VERSION environment variable is required")
if not PHONE_NUMBER_ID:
    raise ValueError("WHATSAPP_PHONE_NUMBER_ID environment variable is required")

def send_message(data: dict):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # Debug logging
    logging.info(f"Sending message to URL: {url}")
    logging.info(f"Headers: {headers}")
    logging.info(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        logging.info(f"Response status: {response.status_code}")
        logging.info(f"Response text: {response.text}")
        response.raise_for_status()
        logging.info("Message sent successfully")
    except requests.Timeout:
        logging.error("Request timed out")
        return json.dumps({"message": "Request timed out", "status": "error"}), 408
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message: {e}")
        logging.error(f"Response status: {getattr(e.response, 'status_code', 'N/A')}")
        logging.error(f"Response text: {getattr(e.response, 'text', 'N/A')}")
        return json.dumps({"message": "Failed to send message", "status": "error"}), 500
    return response
