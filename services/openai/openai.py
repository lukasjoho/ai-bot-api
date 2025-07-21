import os
from openai import AsyncOpenAI
import time
import logging

from services.supabase.supabase import get_conversation, create_conversation

API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = AsyncOpenAI(api_key=API_KEY)

async def generate_openai_response(message: str, wa_id: str):
    conversation = await get_conversation(wa_id)
    if conversation:
        try:
            thread = await client.beta.threads.retrieve(thread_id=conversation["thread_id"])
            logging.info(f"Thread retrieved: {thread.id}")
        except Exception as e:
            logging.error(f"OpenAI thread unexpectedly not found: {e}. Creating new thread...")
            thread = await client.beta.threads.create()
            await create_conversation(wa_id, thread.id)

    else:
        logging.info(f"No thread found in database. Creating new thread...")
        thread = await client.beta.threads.create()
        await create_conversation(wa_id, thread.id)

    message = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    new_message = await run_assistant(thread)
    return new_message


async def check_if_thread_exists(wa_id: str):
    try:
        return await client.beta.threads.retrieve(thread_id=wa_id)
    except Exception as e:
        logging.error(f"Error, trying to retrieve thread: {e}")
        return None

async def run_assistant(thread):
    assistant = await client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)
    run = await client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    
    while run.status not in ["completed", "failed"]:
        time.sleep(0.5)
        run = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = await client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value

    logging.info(f"New message: {new_message}")
    return new_message