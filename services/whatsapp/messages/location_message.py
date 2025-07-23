from services.whatsapp.api import send_message
from services.whatsapp.messages import _create_base_message
from services.whatsapp.types import LocationMessageData

def create_location_message(phone_number: str, data ):
    message = _create_base_message(phone_number, "location")
    message["location"] = {
        "latitude": data.latitude,
        "longitude": data.longitude,
        "name": data.name,
        "address": data.address
    }
    return message

def send_location_message(phone_number: str, data: LocationMessageData):
    data = create_location_message(phone_number, data)
    send_message(data)