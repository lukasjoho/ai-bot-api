from agents import Agent, ModelSettings
from dotenv import load_dotenv
from services.whatsapp.tools import create_communication_tools
from config.config import load_communication_prompt
from services.openai.knowledge_agent import create_knowledge_agent

load_dotenv()

def create_communication_agent(message: str, phone_number: str, message_id: str, name: str, is_new_user: bool):
    # Create knowledge agent as tool
    knowledge_agent = create_knowledge_agent()
    knowledge_retrieval_tool = knowledge_agent.as_tool(
        tool_name="knowledge_retrieval_tool",
        tool_description="Recherchiere spezifische Belcando-Informationen zu Stores, Produkten, Tipps oder Firmendokumenten."
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