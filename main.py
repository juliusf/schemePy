#/usr/local/bin/python3
import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
import sys


while True:
    try:
        expression = rd.parse(input('>'))
        #expression = rd.parse("(let ((a 1) (b 1)) (+ a b))")
        print(ev.evaluate(expression))
    except SchemeException as e:
        print(e)