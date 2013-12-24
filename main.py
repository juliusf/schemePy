import schemepy.reader as rd
import schemepy.evaluator as ev
from schemepy.scheme import *
import sys


while True:
    try:
        expression = rd.parse(input('>'))
        print(ev.evaluate(expression).to_string())
    except SchemeException as e:
        print(e)