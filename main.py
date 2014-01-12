#!/usr/bin/env python3

import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
import sys

sys.setrecursionlimit(100000)

while True:
    try:
        expression = rd.parse(input('>'))
        print(ev.evaluate(expression))
    except SchemeException as e:
        print(e)
    except TypeError as e:
        print(e)
