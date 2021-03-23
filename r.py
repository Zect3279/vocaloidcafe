import redis
import os
import settings

redis_url = settings.REDIS_URL

def connect():
    return redis.from_url(
        url=redis_url, 
        decode_responses=True, 
    )
