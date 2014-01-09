#/usr/local/bin/python3
import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
import sys


while True:
    try:
        #expression = rd.parse(input('>'))
        expression = rd.parse("(cons 1 (cons 1 2))")
        foo = ev.evaluate(expression)
        str(foo)
    except SchemeException as e:
        print(e)
