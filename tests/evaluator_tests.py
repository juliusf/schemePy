from nose.tools import *
from schemepy.scheme import *
import schemepy.evaluator as ev
import schemepy.reader as rd

def test_single_expression_evaluation():
    expression = [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2) ]
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

def test_nested_expression_evaluation():
    expression = [SchemeSymbol('+'), SchemeNumber(1), [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2) ]]
    assert_equal(ev.evaluate(expression), SchemeNumber(4))

def test_primitive_evaluation():
    expression = [SchemeNumber(1)]
    assert_equal(ev.evaluate(expression), 1)

def test_multi_line_evaluation():
    expression = rd.parse("(begin (+ 1 1) (+ 2 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(4))

def test_variable_defines():
    expression = rd.parse("(begin (define x 5) 5)")
    assert_equal(ev.evaluate(expression).value, 5)



