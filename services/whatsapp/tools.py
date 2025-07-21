from functools import partial
from typing import Literal
from agents import function_tool
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_text_message, create_image_message, create_reaction_message, create_location_message, create_cta_message
from services.database.database import get_data

def create_whatsapp_tools(phone_number: str, message_id: str):
    """
    Create WhatsApp function tools with pre-bound phone_number and message_id
    Returns: List of function_tool objects
    """
    
    @function_tool
    def send_text_message(response: str):
        """Send a text message back to the user."""
        data = create_text_message(phone_number, response)
        send_message(data)
    
    @function_tool
    def send_image_message(image_url: str, caption: str = ""):
        """Send an image message back to the user.
        Args:
            image_url: The URL of the image to send to the user.
            caption: The caption of the image to send to the user.
        """
        data = create_image_message(phone_number, image_url, caption)
        send_message(data)
    
    @function_tool
    def send_reaction_message(emoji: str = "👍"):
        """Send a reaction message back to the user.
        Args:
            emoji: The emoji to send to the user. Like 👍, 👎, 🤔, etc.
        """
        data = create_reaction_message(phone_number, message_id, emoji)
        send_message(data)
    
    @function_tool
    def send_location_message(latitude: float, longitude: float, name: str, address: str):
        """Send a location message back to the user.
        Args:
            latitude: The latitude of the location to send to the user.
            longitude: The longitude of the location to send to the user.
            name: The name of the location to send to the user.
            address: The address of the location to send to the user.
        """
        data = create_location_message(phone_number, latitude, longitude, name, address)
        send_message(data)
    
    @function_tool
    def send_cta_message(body_text: str, button_text: str, button_url: str, header_type: Literal["image"] = None, header_content: str = None, footer_text: str = None):
        """Send a CTA message back to the user.
        Args:
            body_text: The body text of the message to send to the user.
            button_text: The text in the button to send to the user.
            button_url: The URL of the button to send to the user.
            header_type: The type of the header to send to the user (image).
            header_content: The content of the header to send to the user.
            footer_text: The text of the footer to send to the user.
        """
        data = create_cta_message(phone_number, body_text, button_text, button_url, header_type, header_content, footer_text)
        send_message(data)
    
    @function_tool
    def get_all_stores():
        """Get all on-site stores from the database."""
        return get_data("stores.json")
    
    @function_tool
    def get_all_products():
        """Get all products from the database."""
        return get_data("products.json")
    
    @function_tool
    def get_all_tips():
        """Get all tips and tricks from the database."""
        return get_data("tipps.json")
    
    return [
        send_text_message, 
        send_image_message, 
        send_reaction_message, 
        send_location_message, 
        send_cta_message,
        get_all_stores, 
        get_all_products, 
        get_all_tips
    ]