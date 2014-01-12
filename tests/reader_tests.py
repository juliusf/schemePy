from nose.tools import *
import imp
import schemepy
from schemepy.scheme import *
import schemepy.reader as rd


def setup_func():
    ev = imp.reload(schemepy)
@with_setup(setup_func)
def test_reader_tokenizer():
    assert_equal(rd._tokenize("(1 2 3)"), ['(', '1', '2', '3', ')'])

@with_setup(setup_func)
def test_reader_parse():
    assert_equal(rd.parse("(+ 2.0 (+ 1 2))"), [SchemeSymbol('begin'), [SchemeSymbol('+'), SchemeNumber(2.0), [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2)]]])

@with_setup(setup_func)
def test_reader_parse_string():
    assert_equal(rd.parse('(define a "teststring with whitespace")'), [SchemeSymbol("begin"), [SchemeSymbol("define"), SchemeSymbol("a"), SchemeString("teststring with whitespace")]])
@with_setup(setup_func)
def test_to_string():
    assert_equal(rd.to_string([SchemeSymbol('+')]), '(+)')
    assert_equal(rd.to_string([SchemeSymbol('+'), SchemeNumber(2.0), [SchemeSymbol('+'), SchemeNumber(1), SchemeNumber(2)]]), "(+ 2.0 (+ 1 2))")

@with_setup(setup_func)
def test_zero_tokens():
    assert_raises(SchemeException, rd.parse, "")