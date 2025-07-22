from agents import Agent, ModelSettings, Runner, trace
from dotenv import load_dotenv
from services.openai.tools.reaction_tools import create_reaction_tools
from config.config import load_reaction_prompt

load_dotenv()

def create_reaction_agent(phone_number: str, message_id: str):
    reaction_tools = create_reaction_tools(phone_number, message_id)
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
    return await Runner.run(reaction_agent, query, previous_response_id=previous_response_id)
    
    