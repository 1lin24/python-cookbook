# coding: utf-8

"""
http://www.ruanyifeng.com/blog/2015/07/monte-carlo-method.html
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import *
import sys
import random
import math

if __name__ == '__main__':
    times = int(sys.argv[1])
    print(sum(math.hypot(random.random(), random.random()) < 1 for i in range(times)) / times * 4)
