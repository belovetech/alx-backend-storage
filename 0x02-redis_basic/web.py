#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import requests
import redis
from functools import wraps
from typing import Callable


_redis = redis.Redis()


# def count_request(method: Callable) -> Callable:
#     """Count number of request sent to a URL"""

#     @wraps(method)
#     def wrapper(*args, **kwargs):
#         """Wrapper function for decorator"""
#         url = str(*args)
#         key = "count:{}".format(str(*args))

#         _redis.incr(key)
#         cache = _redis.get(key)

#         if cache:
#             return cache.decode('utf-8')
#         else:
#             html = method(url)
#             _redis.setex(key, 5, html)
#         return html

#     return wrapper

def count_request(method: Callable) -> Callable:
    """Count number of request sent to a URL"""

    @wraps(method)
    def wrapper(*args, **kwargs):
        # url = str(*args)
        key = "count:{}".format(str(*args))

        _redis.incr(key)
        value = _redis.get(key)
        _redis.expire(key, 10)

        html = method(*args, **kwargs)

        print(f"Time left: {_redis.ttl(key)}")
        return value.decode('utf-8')

    return wrapper


@count_request
def get_page(url: str) -> str:
    """Obtain HTML content through URL"""
    res = requests.get(url)
    return res.text
