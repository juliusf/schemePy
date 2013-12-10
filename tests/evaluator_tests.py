from nose.tools import *
from schemepy.scheme import *
import schemepy.evaluator as ev

def test_evaluate():
	expression = [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2) ]
	assert_equal(ev.evaluate(expression), SchemeNumber(3))