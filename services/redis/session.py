import json
import logging
from typing import List
from services.redis.client import redis_client


class RedisSession:
    """Redis-based session implementation for OpenAI Agents."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis_key = f"session:{session_id}"
        print(f"Created RedisSession with session_id: {session_id}, redis_key: {self.redis_key}")
    
    async def get_items(self, limit: int | None = None) -> List[dict]:
        """Retrieve conversation history for this session."""
        try:
            # Get items from Redis list (most recent first)
            redis_items = await redis_client.lrange(self.redis_key, 0, limit - 1 if limit else -1)
            
            # Convert JSON strings back to dictionaries
            items = []
            for item_json in redis_items:
                try:
                    items.append(json.loads(item_json))
                except json.JSONDecodeError as e:
                    logging.error(f"Failed to parse session item: {e}")
                    continue
            
            return items
        except Exception as e:
            logging.error(f"Error retrieving session items: {e}")
            return []
    
    async def add_items(self, items: List[dict]) -> None:
        """Store new items for this session."""
        try:
            if not items:
                return
                
            # Convert items to JSON and add to Redis list
            json_items = [json.dumps(item, ensure_ascii=False) for item in items]
            
            # Use LPUSH to add items to the front (most recent first)
            await redis_client.lpush(self.redis_key, *json_items)
            
            # Set expiration to 7 days (604800 seconds) for cleanup
            await redis_client.expire(self.redis_key, 604800)
            
            logging.info(f"Added {len(items)} items to session {self.session_id}")
        except Exception as e:
            logging.error(f"Error adding session items: {e}")
            raise
    
    async def pop_item(self) -> dict | None:
        """Remove and return the most recent item from this session."""
        try:
            item_json = await redis_client.lpop(self.redis_key)
            if item_json:
                return json.loads(item_json)
            return None
        except Exception as e:
            logging.error(f"Error popping session item: {e}")
            return None
    
    async def clear_session(self) -> None:
        """Clear all items for this session."""
        try:
            await redis_client.delete(self.redis_key)
            logging.info(f"Cleared session {self.session_id}")
        except Exception as e:
            logging.error(f"Error clearing session: {e}")
            raise
    
    async def get_session_length(self) -> int:
        """Get the number of items in the session."""
        try:
            return await redis_client.llen(self.redis_key)
        except Exception as e:
            logging.error(f"Error getting session length: {e}")
            return 0