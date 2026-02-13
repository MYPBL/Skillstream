import json
import logging
from functools import wraps
from typing import Optional, Any
import redis
from fastapi import Request, Response

logger = logging.getLogger(__name__)

class Cache:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.memory: dict = {}
        try:
            # Try connecting to Redis (short timeout to fail fast)
            self.redis = redis.Redis(host='localhost', port=6379, db=0, socket_connect_timeout=1)
            self.redis.ping()
            logger.info("✅ Redis connected.")
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError, Exception) as e:
            logger.warning(f"⚠️ Redis not available ({e}). Falling back to in-memory cache.")
            self.redis = None

    def get(self, key: str) -> Optional[Any]:
        if self.redis:
            try:
                data = self.redis.get(key)
                return json.loads(data) if data else None
            except Exception:
                return None
        return self.memory.get(key)

    def set(self, key: str, value: Any, expire: int = 60):
        if self.redis:
            try:
                self.redis.setex(key, expire, json.dumps(value))
            except Exception:
                pass
        else:
            self.memory[key] = value
            # In-memory expiration not implemented for simplicity in fallback mode

    def clear(self):
        if self.redis:
            self.redis.flushdb()
        self.memory.clear()

# Global Cache Instance
cache_store = Cache()

def cache(expire: int = 60):
    """
    Simple decorator to cache endpoint responses.
    Cache key is built from URL path.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs if present (common in FastAPI deps)
            # Or inspect args? FastAPI endpoints heavily use kwargs.
            # We need a unique key.
            # For simplicity in this demo, we'll manually use a helper or just check if 'request' is in kwargs.
            request = kwargs.get('request')
            key = None
            if request:
                key = f"cache:{request.url.path}:{request.user.id if hasattr(request, 'user') else 'anon'}"
            
            # If we can't build a key, skip cache
            if not key:
                return await func(*args, **kwargs)

            # Try Get
            cached_data = cache_store.get(key)
            if cached_data:
                logger.info(f"⚡ Cache Hit: {key}")
                return cached_data

            # Call Original
            response = await func(*args, **kwargs)

            # Set
            cache_store.set(key, response, expire)
            return response
        return wrapper
    return decorator

    if cache_store.redis:
        try:
            return cache_store.redis.ping()
        except Exception:
            return False
    return False

async def cache_get(key: str) -> Optional[Any]:
    return cache_store.get(key)

async def cache_set(key: str, value: Any, ttl: int = 60):
    cache_store.set(key, value, expire=ttl)

async def cache_delete(key: str):
    if cache_store.redis:
        try:
            cache_store.redis.delete(key)
        except Exception:
            pass
    if key in cache_store.memory:
        del cache_store.memory[key]
