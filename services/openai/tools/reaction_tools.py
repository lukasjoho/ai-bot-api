from agents import function_tool
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_reaction_message

def create_reaction_tools(phone_number: str, message_id: str):
    @function_tool
    def send_reaction(emoji: str):
        """Sende ein Emoji auf die Nachricht des Nutzers.
        Args:
            emoji: Einzelnes Emoji, das auf die Nachricht des Nutzers gesendet wird (z.B. 🐕, 👍, 🤔, ❤️, 😊, 🎉, etc.)
        """
        data = create_reaction_message(phone_number, message_id, emoji)
        send_message(data)
        return f"Reacted with {emoji}"
    
    @function_tool 
    def no_reaction():
        """Wähle nicht, ein Emoji auf die Nachricht des Nutzers zu senden."""
        return "No reaction sent"
    
    return [send_reaction, no_reaction]