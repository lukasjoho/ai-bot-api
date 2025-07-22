import os
from typing import Literal
from agents import function_tool
from agents.tool import FileSearchTool
from services.database.types import Product, Store, Tip
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_text_message, create_image_message, create_reaction_message, create_location_message, create_cta_message, create_location_request_message, create_interactive_list_message
from services.database.database import get_data

from dotenv import load_dotenv
load_dotenv()

def create_research_tools():

    @function_tool
    def get_all_stores() -> list[Store]:
        """Get all on-site Belcando stores from the database. Can be used to list all, or to get information about only 1 or 2 nearby.
        
        Return example:
        [
            {
                "id": "store_001",
                "name": "Belcando Store Berlin",
                "latitude": 52.52437,
                "longitude": 13.41053,
                "address": {    
                    "street": "Kurfürstendamm 100",
                    "zipcode": "10707",
                    "city": "Berlin"
                }
            }
        ]
        """
        return get_data("stores.json")
    
    @function_tool
    def get_all_products() -> list[Product]:
        """Get all products from the database. Can be used to list all, or to get information about only 1 or 2.
        
        Return example:
        [
            {
                "id": "product_001",
                "imageUrl": "https://d23dsm0lnesl7r.cloudfront.net/media/bc/46/92/1744020374/bb-klp-2023-adult-active-800px.jpg",
                "title": "Dog Box BELCANDO Adult Active",
                "price": "4,99€"
            }
        ]
        """
        return get_data("products.json")
    
    @function_tool
    def get_all_tips() -> list[Tip]:
        """Get all tips and tricks from the database. They are blogposts from the website showing how to take care of your dogs.
        
        Return example:
        
        [
            {
                "id": "tip_001",
                "image": "https://d23dsm0lnesl7r.cloudfront.net/media/6d/09/43/1731491803/blog-puppy-blues.jpg",
                "title": "Von Welpenfreude zu Welpenfrust: Was ist \"Puppy Blues\"?",
                "description": "Wie die anfängliche Freude am neuen Welpen in den 'Puppy Blues' umschlagen kann und wie frischgebackene Hundebesitzer damit umgehen können",
                "url": "https://www.belcando.de/pfotentipps/frust-mit-welpen",
                "cta": "Mehr lesen"
            }
        ]
        """
        return get_data("tips.json")
    
    research_tools = [get_all_stores, get_all_products, get_all_tips]
    
    # Add FileSearchTool if vector store is available
    vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID")
    if vector_store_id:
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store_id])
        research_tools.append(file_search_tool)
    
    return research_tools

def create_communication_tools(phone_number: str, message_id: str):
    
    @function_tool
    def send_text_message(response: str):
        """""Send a text message back to the user. Can be used to send a single text message or multiple text messages. Or in combination with other types of messages (e.g. image, location, reaction, cta)"""""
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
        """React funnily on a user's message. Use any emoji.
        Args:
            emoji: The emoji to send to the user. Like 👍, 👎, 🤔, etc.
        """
        data = create_reaction_message(phone_number, message_id, emoji)
        send_message(data)
    
    @function_tool
    def send_location_message(latitude: float, longitude: float, name: str, address: str):
        """Send a location message back to the user showing a map with a point so that users can better understand a location.
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
        """Send a CTA message back to the user. Such a message "calls for" action and often advertises something.
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
    def send_location_request(body_text: str):
        """Request the user to share their location. For example when they want to find a store or order something to their home adress.
        Args:
            body_text: Text asking for location (e.g., "Bitte teile deinen Standort mit mir")
        """
        data = create_location_request_message(phone_number, body_text)
        send_message(data)
    
    @function_tool
    def send_interactive_questions(body_text: str = "Was kann ich für dich tun? 🐾", button_text: str = "Frage auswählen"):
        """Send an interactive list of questions/topics the user can choose from.
        Important: Send ALWAYS in beginning of conversation with a new user! This gives a user the idea of what to ask.
        Args:
            body_text: Text above the questions list (default: "Was kann ich für dich tun? 🐾")
            button_text: Text on the button to open the list (default: "Frage auswählen")
        """
        # Get questions from database
        questions = get_data("questions.json")
        
        # Format questions as WhatsApp list rows
        rows = []
        for question in questions:
            rows.append({
                "id": question["id"],
                "title": question["title"], 
                "description": question["description"]
            })
        
        # Create sections (WhatsApp requires at least one section)
        sections = [{
            "title": "Wie kann ich dir helfen?",
            "rows": rows
        }]
        
        data = create_interactive_list_message(phone_number, body_text, button_text, sections)
        send_message(data)
    
    return [
        send_text_message, 
        send_image_message, 
        send_reaction_message, 
        send_location_message, 
        send_cta_message,
        send_location_request,
        send_interactive_questions
    ]
    """
    Create WhatsApp function tools with pre-bound phone_number and message_id
    LEGACY: Returns combined research + communication tools for backward compatibility
    """
    
    # Get both research and communication tools
    research_tools = create_research_tools()
    communication_tools = create_communication_tools(phone_number, message_id)
    
    # Return combined list for backward compatibility
    return research_tools + communication_tools