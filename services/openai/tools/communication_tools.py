from typing import Literal
from agents import function_tool
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_text_message, create_image_message, create_location_message, create_cta_message, create_location_request_message, create_interactive_list_message
from services.database.database import get_data

def create_communication_tools(phone_number: str, message_id: str):
    
    @function_tool
    def send_text_message(response: str):
        """Sende eine Textnachricht an den Nutzer. Kann auch in Kombination mit anderen Nachrichtentypen (z.B. Bild, Standort, Reaktion, CTA) verwendet werden.
        
        Args:
            response: Die Textnachricht, die an den Nutzer gesendet werden soll.
        """
        data = create_text_message(phone_number, response)
        send_message(data)
        return "Text message sent"
    
    @function_tool
    def send_image_message(image_url: str, caption: str = ""):
        """Sende ein Bild an den Nutzer mit einer Bildbeschreibung.
        Args:
            image_url: Die URL des Bildes, das an den Nutzer gesendet werden soll.
            caption: Die Bildbeschreibung, die an den Nutzer gesendet werden soll.
        """
        data = create_image_message(phone_number, image_url, caption)
        send_message(data)
        return "Image message sent"

    
    @function_tool
    def send_location_message(latitude: float, longitude: float, name: str, address: str):
        """Sende eine Standortnachricht an den Nutzer, die einen Standort auf einer Karte anzeigt. Nutze diese Funktion um z.B Belcando-Stores anzuzeigen. Kann zum Beispiel dann verwendet werden wenn Nutzer fragen, wo sich ein Belcando-Store befindet oder wo generell verkauft wird.
        
        Args:
            latitude: The latitude of the location to send to the user.
            longitude: The longitude of the location to send to the user.
            name: The name of the location to send to the user.
            address: The address of the location to send to the user.
        """
        data = create_location_message(phone_number, latitude, longitude, name, address)
        send_message(data)
        return "Location message sent"
        
    @function_tool
    def send_cta_message(body_text: str, button_text: str, button_url: str, header_type: Literal["text", "image"] = None, header_content: str = None, footer_text: str = None):
        """Sende eine CTA-Nachricht an den Nutzer. Diese Nachricht "ruft" zu einer Aktion auf und bewirbt oft etwas. Zum Beispiel Blogposts, Kampagnen oder Produkte auf der Belcando-Website.
        
        WICHTIG: Nutze nur gültige Belcando URLs wie https://www.belcando.de, https://www.belcando.de/produkte, etc.

        Wenn du einen header_type "image" verwendest, dann verwende diese URL als header_content: https://d23dsm0lnesl7r.cloudfront.net/media/91/3f/77/1713433379/bb-open-graph-image-BELCANDO.jpeg
        
        Args:
            body_text: Haupttext der Nachricht
            button_text: Text auf dem Button (z.B. "Mehr erfahren", "Zur Website")  
            button_url: Gültige URL zu der der Button führt (nur Belcando URLs!)
            header_type: Optional header type - nur "text" oder "image" erlaubt
            header_content: Header-Inhalt (Text oder gültige Bild-URL mit .jpg, .png, etc.)
            footer_text: Optionaler Footer-Text
        """
        data = create_cta_message(phone_number, body_text, button_text, button_url, header_type, header_content, footer_text)
        send_message(data)
        return "CTA message sent"
        
    @function_tool
    def send_location_request(body_text: str):
        """Request the user to share their location. For example when they want to find a store or order something to their home adress.
        Args:
            body_text: Text asking for location (e.g., "Bitte teile deinen Standort mit mir")
        """
        data = create_location_request_message(phone_number, body_text)
        send_message(data)
        return "Location request sent"
    
    @function_tool
    def send_interactive_questions(body_text: str = "Was kann ich für dich tun? 🐾", button_text: str = "Frage auswählen"):
        """Sende eine interaktive Liste von Fragen/Themen, die der Nutzer auswählen kann.
        Wichtig: Sende IMMER am Anfang einer Konversation mit einem neuen Nutzer! Dies gibt dem Nutzer einen Eindruck davon, was er fragen kann.
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
        return "Interactive questions sent"
        
    return [
        send_text_message, 
        send_image_message, 
        send_location_message, 
        send_cta_message,
        send_location_request,
        send_interactive_questions
    ]