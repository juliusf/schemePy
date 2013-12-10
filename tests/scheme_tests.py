from nose.tools import *
from schemepy.scheme import *

def test_SchemeProcedure():
	proc = SchemeProcedure('test_procedure', ['+', 1, 2])
	assert_equal(proc.name, 'test_procedure')
	assert_equal(proc.impl, ['+', 1, 2])
	assert_equal(proc.type, "Procedure")
	assert_equal(proc.to_string(), "<Procedure:test_procedure>")

def test_SchemeString():
	string = SchemeString('test_string')
	assert_equal(string.value, 'test_string')
	assert_equal(string.type, "String")
	assert_equal(string.to_string(), '"test_string"')

def test_SchemeNumber():
	number = SchemeNumber(3)
	assert_equal(number.value, 3)
	assert_equal(number.type, "Number")
	assert_equal(number.to_string(), '3')

def test_enviornment_find():
	env = Enviornment(['a'], [1])
	assert_equal(1, env.find('a'))

def test_enviornment_find_complex():
	parent_env = Enviornment(['a'],[1])
	env = Enviornment(['b'], [2], parent_env)

	assert_equal(1, env.find('a'))
	assert_raises(Exception, env.find, 'c')

def test_enviornment_update():
	root_env = Enviornment(['a'],[1])
	dict = {'a':2}
	root_env.update(dict)
	assert_equal(root_env.find('a'),2)
