from agents import Agent
from dotenv import load_dotenv
from services.whatsapp.tools import create_knowledge_tools
from config.config import load_knowledge_prompt

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