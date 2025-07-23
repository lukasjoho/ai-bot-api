import openai
from agents import Agent, Runner, trace
from agents.agent_output import AgentOutputSchema
from dotenv import load_dotenv
from config.config import load_system_prompt
from services.openai.agent_tools import create_tools
from services.openai.streamer import process_stream, AgentResponse
from services.whatsapp.messages import send_ratelimit_message, send_exception_message
from services.redis.utils import get_previous_response_id, save_response_id
from services.whatsapp.messages.typing_message import send_typing_indicator
from services.whatsapp.types import TypingMessageData

load_dotenv()

async def run_agent(message: str, message_id: str, phone_number: str, name: str = None):
    try:
        send_typing_indicator(TypingMessageData(message_id=message_id))
        print("Typing indicator sent")
        
        previous_response_id = await get_previous_response_id(phone_number)
        is_new_user = previous_response_id is None
        
        # Create tools and agent
        tools = create_tools(phone_number, message_id)
        agent = Agent(name="Assistant", instructions=load_system_prompt(), tools=tools, output_type=AgentResponse)
        query = f"Antworte auf die Nachricht von {name}. (Neuer Nutzer?: {'Ja' if is_new_user else 'Nein'}). Nachricht: {message}."
        
        with trace("Gregor - WhatsApp Agent"):
            result = Runner.run_streamed(agent, query, previous_response_id=previous_response_id)
            result = await process_stream(result, phone_number)
        
        response_id = result.last_response_id
        if response_id:
            await save_response_id(phone_number, response_id)
        
        return result
        
    except openai.RateLimitError as e:
        send_ratelimit_message(phone_number)
        raise e
    
    except openai.APIError as e:
        # Check if it's a rate limit error by examining the error message
        if "rate limit" in str(e).lower() or "tpm" in str(e).lower():
            send_ratelimit_message(phone_number)
        else:
            send_exception_message(phone_number)
        raise e
    
    except Exception as e:
        send_exception_message(phone_number)  
        raise e