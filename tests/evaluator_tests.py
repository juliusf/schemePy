from nose.tools import *
from schemepy.scheme import *
import schemepy.evaluator as ev
import schemepy.reader as rd


def setup_func():
    ev.reset_enviornment()

@with_setup(setup_func)
def test_single_expression_evaluation():
    expression = [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2) ]
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

@with_setup(setup_func)
def test_nested_expression_evaluation():
    expression = [SchemeSymbol('+'), SchemeNumber(1), [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2) ]]
    assert_equal(ev.evaluate(expression), SchemeNumber(4))

@with_setup(setup_func)
def test_primitive_evaluation():
    expression = [SchemeNumber(1)]
    assert_equal(ev.evaluate(expression), 1)

@with_setup(setup_func)
def test_multi_line_evaluation():
    expression = rd.parse("(begin (+ 1 1) (+ 2 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(4))

@with_setup(setup_func)
def test_variable_defines():
    expression = rd.parse("(begin (define x 5) x)")
    assert_equal(ev.evaluate(expression).value, 5)

@with_setup(setup_func)
def test_lamba():
    expression = rd.parse("(begin (define z (lambda (x y) (+ x y))) (z 1 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

@with_setup(setup_func)
def test_higherorder_functions():
    expression = rd.parse("(begin (define scons (lambda (x y) (lambda (m) (m x y)))) (define scar (lambda (z) (z (lambda (p q) p)))) (scar (scons 10 11)))")
    assert_equal(ev.evaluate(expression), SchemeNumber(10))

@with_setup(setup_func)
def test_enviornments():
    expression = rd.parse("(begin (define b 3) (define fun (lambda (z) b)) (fun 1))")
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

@with_setup(setup_func)
def test_equals():
    expression = rd.parse("(= 3 3)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(= 3 1)")
    assert_equal(ev.evaluate(expression), SchemeFalse())
    expression = rd.parse("(= 3 3 3)")
    assert_equal(ev.evaluate(expression), SchemeTrue())
    expression = rd.parse("(= 3 1 1)")
    assert_equals(ev.evaluate(expression), SchemeFalse())

@with_setup(setup_func)
def test_if():
    expression = rd.parse("(if (= 3 3) 1 2)")
    assert_equal(ev.evaluate(expression), SchemeNumber(1))
    expression = rd.parse("(if (= 3 1) 1 2)")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))
