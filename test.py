#!/usr/bin/env python3
from nose.tools import *
import schemepy
import imp
from schemepy.scheme import *
import schemepy.evaluator as ev
import schemepy.reader as rd
import schemepy.transpiler as tr
expr = rd.parse("(+ 3 2 (+ 3 2))")
foo = tr.transpile(expr)
print(foo)
