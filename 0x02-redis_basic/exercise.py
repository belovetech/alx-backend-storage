#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
from typing import Union
import uuid


class Cache:
    """Cache class representation"""

    def __init__(self) -> None:
        """Initialize redis instance and flush db"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data into catch

        Args:
            data(Union[str, int, float, bytes]): value to store

        Return:
            (str): Key of the value store
        """
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key
