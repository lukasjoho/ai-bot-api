import os
import requests
import logging
import json
from dotenv import load_dotenv


load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
VERSION = os.getenv("WHATSAPP_API_VERSION")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
RECIPIENT_WAID = os.getenv("WHATSAPP_RECIPIENT_DEMO_WAID")

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
