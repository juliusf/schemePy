from nose.tools import *
import schemepy.reader as rd


def setup():
    print("SETUP!")

def teardown():
    print ("TEAR DOWN!")

def test_reader_tokenizer():
    assert_equal(rd._tokenize("(1 2 3)"), ['(', '1', '2', '3', ')'])

def test_reader_parse():
	assert_equal(rd.parse("(+ 2.0 (+ 1 2))"), ['+', 2.0, ['+', 1, 2]])

def test_to_string():
	assert_equal(rd.to_string(['+']), '(+)')
	assert_equal(rd.to_string(['+', 2.0, ['+', 1, 2]]), "(+ 2.0 (+ 1 2))")