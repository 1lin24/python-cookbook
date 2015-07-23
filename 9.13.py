# coding: utf-8


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super(Singleton, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Spam():
    __metaclass__ = Singleton
    def __init__(self):
        print('Creating Spam')


a = Spam()
b = Spam()

print a is b
