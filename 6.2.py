# coding: utf-8

class MyDict:

    def __init__(self, d):
        self.__dict__ = d




mydict = MyDict({'a': 1})
print mydict.a
