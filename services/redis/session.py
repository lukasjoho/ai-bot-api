import json
from typing import List
from agents.items import TResponseInputItem
from .client import redis_client

class MyCustomSession:
    """Custom session implementation following the Session protocol."""

    def __init__(self, session_id: str):
        self.session_id = session_id

    async def get_items(self, limit: int | None = None) -> List[TResponseInputItem]:
        print(f"Getting items for session: {self.session_id}")
        """Retrieve conversation history for this session."""
        if limit is None:
            raw_items = await redis_client.lrange(self.session_id, 0, -1)
        else:
            raw_items = await redis_client.lrange(self.session_id, -limit, -1)
        
        items = []
        for raw_item in raw_items:
            item = json.loads(raw_item)
            items.append(item)
        
        return items

    async def add_items(self, items: List[TResponseInputItem]) -> None:
        print(f"Adding items for session: {self.session_id}")
        """Store new items for this session."""
        if not items:
            return
        
        serialized_items = [json.dumps(item) for item in items]
        await redis_client.rpush(self.session_id, *serialized_items)
        print(f"Added items for session: {self.session_id}")

    async def pop_item(self) -> TResponseInputItem | None:
        print(f"Popping item for session: {self.session_id}")
        """Remove and return the most recent item from this session."""
        raw_item = await redis_client.rpop(self.session_id)
        if raw_item is None:
            return None
        
        return json.loads(raw_item)

    async def clear_session(self) -> None:
        print(f"Clearing session: {self.session_id}")
        """Clear all items for this session."""
        await redis_client.delete(self.session_id)