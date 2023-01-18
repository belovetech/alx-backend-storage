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
        """Wrapper function for decorator"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Store history of input and output of a particular method"""
    key = method.__qualname__
    keyinput = key + ":inputs"
    keyoutput = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for decorator"""
        self._redis.rpush(keyinput, str(args))
        value = method(self, *args, **kwargs)
        self._redis.rpush(keyoutput, str(value))
        return value

    return wrapper


def replay(method: Callable) -> None:
    """Replay the history of a method"""
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode('utf-8')
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)

    for i, o in zip(inputs, outputs):
        i = i.decode('utf-8')
        o = o.decode('utf-8')
        print("{}(*{}) -> {}".format(name, i, o))


class Cache:
    """Cache class representation"""

    def __init__(self) -> None:
        """Initialize redis instance and flush db"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data into catch

        Args:
            data(Union[str, int, float, bytes]): value to store

        Return:
            (str): Key of the value store
        """
        key = str(uuid.uuid4())
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
