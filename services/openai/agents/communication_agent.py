from agents import Agent, ModelSettings, Runner
from dotenv import load_dotenv
from services.openai.tools.communication_tools import create_communication_tools
from config.config import load_communication_prompt
from services.openai.agents.knowledge_agent import create_knowledge_agent

load_dotenv()

def create_communication_agent(message: str, phone_number: str, message_id: str, name: str, is_new_user: bool):
    # Create knowledge agent as tool
    knowledge_agent = create_knowledge_agent()
    knowledge_retrieval_tool = knowledge_agent.as_tool(
        tool_name="knowledge_retrieval_tool",
        tool_description="Recherchiere spezifische Belcando-Informationen zu Stores, Produkten, Tipps oder Firmendokumenten.",
    )
    
    # Get WhatsApp communication tools
    whatsapp_tools = create_communication_tools(phone_number, message_id)
    
    # Combine all tools
    all_tools = whatsapp_tools + [knowledge_retrieval_tool]
    
    # Load communication prompt
    communication_prompt = load_communication_prompt(message, name, is_new_user)
    
    return Agent(
        name="Gregor von Belcando",
        instructions=communication_prompt,
        tools=all_tools,
        model="gpt-4o",
        model_settings=ModelSettings(tool_choice="required")
    )

async def run_communication_agent(message: str, phone_number: str, message_id: str, name: str, is_new_user: bool, previous_response_id: str | None):
    communication_agent = create_communication_agent(message, phone_number, message_id, name, is_new_user)
    query = f"Antworte auf diese Nachricht von {name}: {message}. (Neuer Nutzer?: {'Ja' if is_new_user else 'Nein'})"
    
    return await Runner.run(communication_agent, query, previous_response_id=previous_response_id)
