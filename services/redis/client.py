import os
import httpx
import logging
from typing import Optional, List, Any
from dotenv import load_dotenv

load_dotenv()

class UpstashRedisClient:
    def __init__(self):
        self.rest_url = os.getenv("UPSTASH_REDIS_REST_URL")
        self.rest_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        
        if not self.rest_url or not self.rest_token:
            raise ValueError("UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN must be set")
        
        self.headers = {
            "Authorization": f"Bearer {self.rest_token}",
            "Content-Type": "application/json"
        }
    
    async def _execute_command(self, command: List[str]) -> Any:
        """Execute a Redis command via Upstash REST API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.rest_url,
                    headers=self.headers,
                    json=command,
                    timeout=10.0
                )
                response.raise_for_status()
                result = response.json()
                return result.get("result")
            except httpx.HTTPError as e:
                logging.error(f"Redis command failed: {e}")
                raise    

    async def get(self, key: str) -> Optional[str]:
        """Get the value of a key"""
        command = ["GET", key]
        return await self._execute_command(command)
    
    async def set(self, key: str, value: str) -> str:
        """Set the value of a key"""
        command = ["SET", key, value]
        return await self._execute_command(command)

# Global client instance
redis_client = UpstashRedisClient()