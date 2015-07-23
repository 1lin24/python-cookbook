

def make_handler():

    sequence = 0
    while True:
        result = yield
        sequence += 1
        print '[{}] Got: {}'.format(sequence, result)


handler = make_handler()
next(handler)


def apply_async(func, args, callback):
    result = func(*args)
    callback(result)

def add(x, y):
    return x + y

apply_async(add, (1, 2), callback=handler.send)
apply_async(add, (1, 2), callback=handler.send)
