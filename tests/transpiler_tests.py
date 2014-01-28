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