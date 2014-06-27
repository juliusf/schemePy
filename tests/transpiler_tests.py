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
def test_basic_arithmetics():
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
def test_simple_if():
    expr = rd.parse('(if (< 3 2) #t #f)')
    assert_equal(exec(tr.transpile(expr)), False)
