from redis import Redis
from typing import Optional
import json
import os

# Test ortamı kontrolü
IS_TESTING = os.getenv('TESTING', 'false').lower() == 'true'

if not IS_TESTING:
    redis_client = Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=0,
        decode_responses=True
    )
else:
    # Test ortamı için mock Redis client
    class MockRedis:
        def __init__(self):
            self.data = {}
        
        def setex(self, key, time, value):
            self.data[key] = value
            return True
        
        def get(self, key):
            return self.data.get(key)
        
        def delete(self, *keys):
            for key in keys:
                self.data.pop(key, None)
            return True

    redis_client = MockRedis()

class URLCache:
    @staticmethod
    async def set_url(short_code: str, url_data: dict, expire_time: int = 3600):
        """URL verisini cache'e kaydet"""
        try:
            return redis_client.setex(
                f"url:{short_code}",
                expire_time,
                json.dumps(url_data)
            )
        except Exception:
            return False

    @staticmethod
    async def get_url(short_code: str) -> Optional[dict]:
        """Cache'den URL verisini al"""
        try:
            data = redis_client.get(f"url:{short_code}")
            return json.loads(data) if data else None
        except Exception:
            return None

    @staticmethod
    async def increment_clicks(short_code: str):
        """Tıklama sayısını artır"""
        pass

    @staticmethod
    async def get_clicks(short_code: str) -> int:
        """Cache'den tıklama sayısını al"""
        return 0

    @staticmethod
    async def clear_cache(short_code: str):
        """URL için cache'i temizle"""
        try:
            redis_client.delete(f"url:{short_code}")
            return True
        except Exception:
            return False 