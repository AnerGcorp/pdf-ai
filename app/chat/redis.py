import os
import redis

client = redis.Redis.from_url(
    os.getenv['REDIS_URI'],
    decode_responses=True
)