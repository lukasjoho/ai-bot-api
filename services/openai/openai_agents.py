import os
from agents import Agent, Runner
from dotenv import load_dotenv
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_typing_indicator
from services.whatsapp.tools import create_whatsapp_tools
from services.redis.session import RedisSession
from config.config import load_system_prompt

load_dotenv()

async def run_agent(message: str, message_id: str, phone_number: str, name: str):
    print(f"Running agent for name: {name} phone: {phone_number} with message: {message} with id: {message_id}")

    # Send typing indicator immediately
    typing_data = create_typing_indicator(message_id)
    send_message(typing_data)
    
    # Create session for persistent memory
    session = RedisSession(session_id=phone_number)
    
    # Create tools with pre-bound phone_number and message_id
    tools = create_whatsapp_tools(phone_number, message_id)
    
    system_prompt = load_system_prompt()
    print(f"System prompt loaded...")
    agent = Agent(name="Gregor von Belcando", instructions=system_prompt, tools=tools)
    print(f"Agent created...")
    
    print(f"Running agent with session...")
    result = await Runner.run(agent, message, session=session)
    print(f"Agent run completed... Used tools: {len(result.raw_responses)}")
    
    return result.final_output