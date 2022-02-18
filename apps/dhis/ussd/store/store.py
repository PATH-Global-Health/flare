import json
import redis

from django.conf import settings


class Store:
    redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT, db=0, decode_responses=True)

    def __init__(self):
        pass

    @classmethod
    def exists(cls, key):
        return cls.redis_instance.exists(key)

    @classmethod
    def get(cls, key):
        return json.loads(cls.redis_instance.get(key))

    @classmethod
    def set(cls, key, data):
        cls.redis_instance.set(key, json.dumps(data))

    @classmethod
    def unlink(cls, key):
        if Store.exists(key):
            cls.redis_instance.unlink(key)

    @classmethod
    def delete(cls, key):
        if Store.exists(key):
            cls.redis_instance.delete(key)
