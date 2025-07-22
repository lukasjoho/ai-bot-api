import openai
from agents import Runner, trace
from dotenv import load_dotenv
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_typing_indicator, create_text_message
from services.redis.utils import get_previous_response_id, save_response_id
from services.openai.communication_agent import create_communication_agent
from services.openai.reaction_agent import run_reaction_agent

load_dotenv()

async def run_agents(message: str, message_id: str, phone_number: str, name: str):
    try:
        # Send typing indicator immediately
        typing_data = create_typing_indicator(message_id)
        send_message(typing_data)
        
        previous_response_id = await get_previous_response_id(phone_number)
        is_new_user = previous_response_id is None
        
        with trace("Gregor - Complete Workflow"):
            # First: Run reaction agent for quick emoji response
            reaction_response_id = await run_reaction_agent(message, phone_number, message_id, previous_response_id)
            
            # Create communication agent with knowledge tool  
            communication_agent = create_communication_agent(message, phone_number, message_id, name, is_new_user)

            query = f"Antworte auf diese Nachricht von {name}: {message}. (Neuer Nutzer?: {'Ja' if is_new_user else 'Nein'})"
            
            # Use reaction_response_id to continue the conversation chain
            result = await Runner.run(communication_agent, query, previous_response_id=reaction_response_id)
        
        if result.last_response_id:
            await save_response_id(phone_number, result.last_response_id)
        
        return result.final_output
        
    except openai.RateLimitError as e:
        # Send friendly rate limit message to user
        error_message = "Wuff! 🐕 Mir qualmt gerade der Kopf - zu viele Fragen auf einmal! Gib mir kurz 1 Minute Pause und versuche es dann nochmal. Danke für dein Verständnis! 🐾"
        
        error_data = create_text_message(phone_number, error_message)
        send_message(error_data)
        
        # Re-raise for logging purposes
        raise e
    
    except Exception as e:
        # Send generic error message for other exceptions
        error_message = "Wuff! 🐕 Da ist wohl was schiefgelaufen... Kannst du deine Nachricht nochmal schicken? Ich bin gleich wieder da! 🐾"
        
        error_data = create_text_message(phone_number, error_message)
        send_message(error_data)
        
        # Re-raise for logging purposes
        raise e