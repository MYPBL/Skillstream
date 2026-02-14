"""
Flush Redis Cache.
Run this after manual DB updates to ensure API serves fresh data.
"""
import redis
from app.core.config import settings

def flush_cache():
    try:
        r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        r.flushall()
        print("✅ Redis Cache Flushed Successfully!")
    except Exception as e:
        print(f"❌ Failed to flush cache: {e}")

if __name__ == "__main__":
    flush_cache()
