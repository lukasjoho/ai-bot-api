from agents import Agent, ModelSettings, Runner, function_tool, trace
from dotenv import load_dotenv
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_reaction_message
from config.config import load_reaction_prompt

load_dotenv()

def create_reaction_tool(phone_number: str, message_id: str):
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

def create_reaction_agent(phone_number: str, message_id: str):
    reaction_tools = create_reaction_tool(phone_number, message_id)
    reaction_prompt = load_reaction_prompt()

    return Agent(
        name="Gregor - Reaction",
        instructions=reaction_prompt,
        tools=reaction_tools,
        model="gpt-4o-mini",
        model_settings=ModelSettings(tool_choice="required")
    )

async def run_reaction_agent(message: str, phone_number: str, message_id: str, previous_response_id: str | None):
    reaction_agent = create_reaction_agent(phone_number, message_id)
    query = f"Nachricht vom Nutzer: '{message}'"
    
    with trace("Gregor - Reaction"):
        result = await Runner.run(reaction_agent, query, previous_response_id=previous_response_id)
    
    return result.last_response_id