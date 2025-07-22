import os
from agents import Agent, ModelSettings, Runner, model_settings
from dotenv import load_dotenv
from services.whatsapp.api import send_message
from services.whatsapp.messages import create_typing_indicator
from services.whatsapp.tools import create_whatsapp_tools
from services.redis.client import redis_client
from config.config import load_system_prompt

load_dotenv()

async def get_previous_response_id(phone_number: str) -> str | None:
    """Get the last response ID for this phone number from Redis."""
    key = f"response_id:{phone_number}"
    response_id = await redis_client.get(key)
    return response_id

async def save_response_id(phone_number: str, response_id: str) -> None:
    """Save the response ID for this phone number to Redis."""
    key = f"response_id:{phone_number}"
    await redis_client.set(key, response_id)
    # Optional: Set expiration (e.g., 7 days)
    await redis_client.expire(key, 604800)

async def run_agent(message: str, message_id: str, phone_number: str, name: str):
    print(f"Running agent for name: {name} phone: {phone_number} with message: {message} with id: {message_id}")

    # Send typing indicator immediately
    typing_data = create_typing_indicator(message_id)
    send_message(typing_data)
    
    # Get previous response ID for conversation continuity
    previous_response_id = await get_previous_response_id(phone_number)
    print(f"Previous response ID: {previous_response_id}")
    
    # Create tools with pre-bound phone_number and message_id
    tools = create_whatsapp_tools(phone_number, message_id)

    # is_new_user = previous_response_id is None
    is_new_user = True
    
    system_prompt = load_system_prompt(is_new_user)
    print(f"System prompt loaded...")
    agent = Agent(
        name="Gregor von Belcando", 
        instructions=system_prompt, 
        tools=tools,
        model_settings=ModelSettings(tool_choice="required")
    )
    print(f"Agent created...")

    # Run agent with previous_response_id for conversation continuity
    print(f"Running agent with previous_response_id: {previous_response_id}")
    result = await Runner.run(agent, message, previous_response_id=previous_response_id)
    
    # Save the new response ID for next conversation turn
    if result.last_response_id:
        await save_response_id(phone_number, result.last_response_id)
        print(f"Saved response ID: {result.last_response_id}")
    
    print(f"Agent run completed")
    return result.final_output