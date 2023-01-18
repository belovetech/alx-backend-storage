#!/usr/bin/env python3
"""Writing strings to Redis"""
from functools import wraps
import redis
from typing import Union, Optional, Callable
import uuid


def count_calls(method: Callable) -> Callable:
    """Count Cache class methods calls."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache class representation"""

    def __init__(self) -> None:
        """Initialize redis instance and flush db"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Convert key to the desired format"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, value: bytes) -> str:
        """Get str from the cache"""
        return str(value.decode('utf-8'))

    def get_int(self, value: bytes) -> int:
        """Get int from the cache"""
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
