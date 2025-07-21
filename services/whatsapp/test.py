from dotenv import load_dotenv
import os
import requests

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

if __name__ == "__main__":
    send_whatsapp_message()


