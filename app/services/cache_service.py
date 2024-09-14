import redis
from typing import Any, Optional

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        return self.redis.get(key)

    async def set(self, key: str, value: Any, expiration: int = 3600):
        self.redis.set(key, value, ex=expiration)

    async def delete(self, key: str):
        self.redis.delete(key)
