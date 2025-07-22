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
    
    async def lpush(self, key: str, *values: str) -> int:
        """Push values to the left of a list"""
        command = ["LPUSH", key] + list(values)
        return await self._execute_command(command)
    
    async def rpush(self, key: str, *values: str) -> int:
        """Push values to the right of a list"""
        command = ["RPUSH", key] + list(values)
        return await self._execute_command(command)
    
    async def lrange(self, key: str, start: int, stop: int) -> List[str]:
        """Get a range of elements from a list"""
        command = ["LRANGE", key, str(start), str(stop)]
        result = await self._execute_command(command)
        return result or []
    
    async def lpop(self, key: str) -> Optional[str]:
        """Remove and return the first element of a list"""
        command = ["LPOP", key]
        return await self._execute_command(command)
    
    async def rpop(self, key: str) -> Optional[str]:
        """Remove and return the last element of a list"""
        command = ["RPOP", key]
        return await self._execute_command(command)
    
    async def delete(self, key: str) -> int:
        """Delete a key"""
        command = ["DEL", key]
        return await self._execute_command(command)
    
    async def llen(self, key: str) -> int:
        """Get the length of a list"""
        command = ["LLEN", key]
        result = await self._execute_command(command)
        return result or 0
    
    async def expire(self, key: str, seconds: int) -> int:
        """Set expiration time for a key"""
        command = ["EXPIRE", key, str(seconds)]
        return await self._execute_command(command)
    
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