# coding: utf-8

from __future__ import print_function
import time
from functools import wraps


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(end - start)
    return wrapper

@timethis
def test():
    time.sleep(1)

print(test.__name__)
print(dir(test))
print(test.__wrapped__)
test()
