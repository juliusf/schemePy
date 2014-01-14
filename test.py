#!/usr/bin/env python3

import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
import sys

sys.setrecursionlimit(100000)

define_test =rd.parse("""
                                  ((lambda (x)
                                      (+((lambda ()
                                          (define x 1)
                                          x
                                      )) x)
                                  ) 2)
                          """)

print(ev.evaluate(define_test))
