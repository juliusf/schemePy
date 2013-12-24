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
def test_lambda_exception():
    expression = rd.parse("(lambda (x y z) )")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_lambda_no_params():
    expression = rd.parse("(begin (define foo (lambda () (+ 1 1))) (foo)) ")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))

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

@with_setup(setup_func)
def test_if_exeption():
    expression = rd.parse("(if (= 1 1) 1)")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_cons():
    expression = rd.parse("(cons 1 2)")
    assert_equal = (ev.evaluate(expression), SchemeCons(1,2))

@with_setup(setup_func)
def test_cons_exception():
    expression = rd.parse("(cons 1)")
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_car():
    expression = rd.parse("(car (cons 1 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(1))

@with_setup(setup_func)
def test_car_exception():
    expression = rd.parse('(car (cons 1 2) (cons 1 2))')
    assert_raises(SchemeException, ev.evaluate, expression)

    expression = rd.parse('(car 1)')
    assert_raises(SchemeException, ev.evaluate, expression)

@with_setup(setup_func)
def test_cdr():
    expression = rd.parse("(cdr (cons 1 2))")
    assert_equal(ev.evaluate(expression), SchemeNumber(2))

@with_setup(setup_func)
def test_cdr_exception():
    expression = rd.parse('(cdr (cons 1 2) (cons 1 2))')
    assert_raises(SchemeException, ev.evaluate, expression)

    expression = rd.parse('(cdr 1)')
    assert_raises(SchemeException, ev.evaluate, expression)