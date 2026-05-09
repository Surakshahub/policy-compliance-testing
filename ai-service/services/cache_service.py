import redis
import hashlib
import json


class CacheService:

    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

    TTL = 900

    @staticmethod
    def generate_key(text):

        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def get(text):

        key = CacheService.generate_key(text)

        cached = CacheService.redis_client.get(key)

        if cached:
            return json.loads(cached)

        return None

    @staticmethod
    def set(text, value):

        key = CacheService.generate_key(text)

        CacheService.redis_client.setex(
            key,
            CacheService.TTL,
            json.dumps(value)
        )