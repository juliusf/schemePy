#!/usr/bin/env python3


import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
from schemepy.stream import Stream


inp = '(define (add a b) (+ a b)) (add 2 3)'
foo = rd.parse(inp)
print(foo)
