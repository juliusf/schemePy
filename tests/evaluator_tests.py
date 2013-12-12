from nose.tools import *
from schemepy.scheme import *
import schemepy.evaluator as ev
import schemepy.reader as rd


def setup_func():
    ev._root_environment = SchemeEnvironment()
    ev.root_environment.update(ev.builtin_functions)
    print("assholr")

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
    expression = rd.parse("(begin (define x 3) (define fun (lambda (z) x)) (fun 1))")
    assert_equal(ev.evaluate(expression), SchemeNumber(3))

