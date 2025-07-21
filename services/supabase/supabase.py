import os
from supabase import acreate_client, AsyncClient
import logging

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_API_KEY")

async def init_supabase():
    return await acreate_client(url, key)

supabase: AsyncClient = None

async def get_supabase() -> AsyncClient:
    global supabase
    return supabase if supabase else await init_supabase()

async def get_conversation(wa_id: str):
    client = await get_supabase()
    result = await client.table("conversation").select("thread_id").eq("wa_id", wa_id).execute()
    return result.data[0] if result.data else None

async def create_conversation(wa_id: str, thread_id: str):
    try:
        client = await get_supabase()
        result = await client.table("conversation").upsert({"wa_id": wa_id, "thread_id": thread_id}, on_conflict="wa_id").execute()
        logging.info(f"Conversation upserted for wa_id: {wa_id} and thread_id: {thread_id}")
        return result.data[0]
    except Exception as e:
        logging.error(f"Error creating conversation: {e}")
        raise e
