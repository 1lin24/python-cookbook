# coding: utf-8

from __future__ import print_function
import weakref

class Spam:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

_span_cache = weakref.WeakValueDictionary()
def get_spam(name):
    if name in _span_cache:
        return _span_cache[name]
    else:
        spam = Spam(name)
        _span_cache[name] = spam
        return spam

a = get_spam('foo')
b = get_spam('bar')
print(_span_cache.items())
