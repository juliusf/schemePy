from nose.tools import *
import schemepy
import imp
from schemepy.scheme import *
import schemepy.evaluator as ev
import schemepy.reader as rd
import schemepy.transpiler as tr


def setup_func():
    ev = imp.reload(schemepy)

@with_setup(setup_func)
def test_basic_arithmetic():
    expr = rd.parse("(+ 3 2)")
    assert_equal(tr.transpile(expr), "3 + 2\n")

    expr = rd.parse("(+ 3 2 (+ 3 2))")
    assert_equal(tr.transpile(expr),  "3 + 2 + ( 3 + 2 )\n")

    expr = rd.parse("(+ (+ 3 2) 2)")
    assert_equal(tr.transpile(expr), "( 3 + 2 ) + 2\n")

    expr = rd.parse("(+ (* 3 2) 2)")
    assert_equal(tr.transpile(expr), "( 3 * 2 ) + 2\n")

    assert_equal(eval(tr.transpile(expr)), 8)

    expr = rd.parse("(+ 3 3 3)")
    assert_equal(eval(tr.transpile(expr)), 9)


@with_setup(setup_func)
def test_begin():
    expr = rd.parse("(begin (+ 3 2) (+ 1 2)")
    assert_equal(tr.transpile(expr), "3 + 2\n1 + 2\n\n")

@with_setup(setup_func)
def test_simple_if():
    expr = rd.parse('(if (< 3 2) #t #f)')
    assert_equal(tr.transpile(expr), 'if 3 < 2:\n    True\nelse:\n    False\n\n')


@with_setup(setup_func)
def test_simple_define():
    expr = rd.parse("(define x 1)")
    assert_equal(tr.transpile(expr), 'x = 1\n')

    expr = rd.parse('(if (< 3 2) (define x 1) (define x 2))')
    assert_equal(tr.transpile(expr), 'if 3 < 2:\n    x = 1\nelse:\n    x = 2\n\n')