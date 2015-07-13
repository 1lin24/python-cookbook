# coding: utf-8

from collections import deque


class LineHistory:

    def __init__(self, lines, hislen=3):
        self.lines = lines
        self.history = deque(maxlen=hislen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()


gen = iter('abcdefghijklmn')
lines = LineHistory(gen)
for line in lines:
    print line, lines.history
