from services.redis.client import redis_client


async def get_previous_response_id(phone_number: str) -> str | None:
    key = f"response_id:{phone_number}"
    response_id = await redis_client.get(key)
    return response_id

async def save_response_id(phone_number: str, response_id: str) -> None:
    key = f"response_id:{phone_number}"
    await redis_client.set(key, response_id)
    await redis_client.expire(key, 604800)