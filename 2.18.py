# coding: utf-8

import re
from collections import namedtuple


text = 'foo = 23 + 42 * 10'

NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

pattern = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pattern, text):
    scanner = pattern.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())


for token in generate_tokens(pattern, text):
    if token.type != 'WS':
        print token
