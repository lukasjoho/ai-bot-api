from agents import Agent, ModelSettings, Runner, trace
from dotenv import load_dotenv
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_typing_indicator
from services.whatsapp.tools import create_research_tools, create_communication_tools
from services.redis.utils import get_previous_response_id, save_response_id
from config.config import load_system_prompt, load_knowledge_prompt, load_communication_prompt

load_dotenv()

async def run_knowledge_agent(query: str, previous_response_id: str | None):
    research_tools = create_research_tools()
    research_prompt = load_knowledge_prompt()
    
    agent = Agent(
        name="Gregor - Knowledge",
        instructions=research_prompt,
        tools=research_tools,
        model="gpt-4o",
    ) 
    return await Runner.run(agent, query, previous_response_id=previous_response_id)


async def run_communication_agent(research_data: str, original_message: str, phone_number: str, message_id: str, name: str, is_new_user: bool, knowledge_response_id: str | None):
    typing_data = create_typing_indicator(message_id)
    send_message(typing_data)
    
    communication_tools = create_communication_tools(phone_number, message_id)
    communication_prompt = load_communication_prompt(research_data, original_message, name, is_new_user)

    agent = Agent(
        name="Gregor - Communication",
        instructions=communication_prompt,
        tools=communication_tools,
        model="gpt-4o",
        model_settings=ModelSettings(tool_choice="required")
    )
    
    query = f"Antworte auf die Nachricht '{original_message}' basierend auf den Forschungsdaten."
    return await Runner.run(agent, query, previous_response_id=knowledge_response_id)

async def run_agents(message: str, message_id: str, phone_number: str, name: str):
    previous_response_id = await get_previous_response_id(phone_number)
    is_new_user = previous_response_id is None
    
    with trace("Gregor - Agent Workflow"):
        knowledge_result = await run_knowledge_agent(message, previous_response_id)
    
        communication_result = await run_communication_agent(
            research_data=knowledge_result.final_output,
            original_message=message,
            phone_number=phone_number,
            message_id=message_id,
            name=name,
            is_new_user=is_new_user,
            knowledge_response_id=knowledge_result.last_response_id
        )
    
    if communication_result.last_response_id:
        await save_response_id(phone_number, communication_result.last_response_id)
    
    return communication_result