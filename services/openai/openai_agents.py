import openai
from agents import Agent, ModelSettings, Runner, trace
from dotenv import load_dotenv
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_typing_indicator, create_text_message
from services.whatsapp.tools import create_knowledge_tools, create_communication_tools
from services.redis.utils import get_previous_response_id, save_response_id
from config.config import load_knowledge_prompt, load_communication_prompt, load_orchestration_prompt

load_dotenv()

def create_knowledge_agent():
    knowledge_tools = create_knowledge_tools()
    knowledge_prompt = load_knowledge_prompt()
    
    return Agent(
        name="Gregor - Knowledge",
        instructions=knowledge_prompt,
        tools=knowledge_tools,
        model="gpt-4o",
    )

def create_communication_agent(phone_number: str, message_id: str, name: str, is_new_user: bool):
    communication_tools = create_communication_tools(phone_number, message_id)
    communication_prompt = load_communication_prompt(name, is_new_user)
    
    return Agent(
        name="Gregor - Communication",
        instructions=communication_prompt,
        tools=communication_tools,
        model="gpt-4o",
        model_settings=ModelSettings(tool_choice="required")
    )

def create_orchestration_agent(message: str, name: str, is_new_user: bool, phone_number: str, message_id: str):
    # Create knowledge and communication agents as tools
    knowledge_agent = create_knowledge_agent()
    knowledge_retrieval_tool = knowledge_agent.as_tool(
        tool_name="knowledge_retrieval_tool",
        tool_description="Recherchiere spezifische Belcando-Informationen zu Stores, Produkten, Tipps oder Firmendokumenten."
    )
    
    communication_agent = create_communication_agent(phone_number, message_id, name, is_new_user)
    communication_tool = communication_agent.as_tool(
        tool_name="communication_tool",
        tool_description="Sende deine Antwort als WhatsApp-Nachricht an den Nutzer. Du MUSST dieses Tool verwenden um zu antworten!"
    )
    
    # Load orchestration prompt
    orchestration_prompt = load_orchestration_prompt(message, name, is_new_user)
    
    return Agent(
        name="Gregor von Belcando",
        instructions=orchestration_prompt,
        tools=[knowledge_retrieval_tool, communication_tool],
        model="gpt-4o",
        model_settings=ModelSettings(tool_choice="communication_tool")
    )

async def run_agents(message: str, message_id: str, phone_number: str, name: str):
    try:
        # Send typing indicator immediately
        typing_data = create_typing_indicator(message_id)
        send_message(typing_data)
        
        previous_response_id = await get_previous_response_id(phone_number)
        is_new_user = previous_response_id is None
        
        # Create orchestration agent with knowledge and communication as tools
        orchestration_agent = create_orchestration_agent(message, name, is_new_user, phone_number, message_id)
        
        with trace("Gregor - Orchestration Workflow"):
            result = await Runner.run(orchestration_agent, message, previous_response_id=previous_response_id)
        
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