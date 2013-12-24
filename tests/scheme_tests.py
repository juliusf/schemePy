from nose.tools import *
from schemepy.scheme import *
import schemepy.evaluator as ev

def setup_func():
    ev._root_environment = SchemeEnvironment()
    ev.root_environment.update(ev.builtin_functions)

@with_setup(setup_func)
def test_SchemeProcedure():
    proc = SchemeProcedure('test_procedure', ['+', 1, 2])
    assert_equal(proc.name, 'test_procedure')
    assert_equal(proc.impl, ['+', 1, 2])
    assert_equal(proc.type, "Procedure")
    assert_equal(proc.to_string(), "<Procedure:test_procedure>")

@with_setup(setup_func)
def test_SchemeString():
    string = SchemeString('test_string')
    assert_equal(string.value, 'test_string')
    assert_equal(string.type, "String")
    assert_equal(string.to_string(), '"test_string"')

@with_setup(setup_func)
def test_SchemeNumber():
    number = SchemeNumber(3)
    assert_equal(number.value, 3)
    assert_equal(number.type, "Number")
    assert_equal(number.to_string(), '3')

@with_setup(setup_func)
def test_SchemeBoolean():
    true = SchemeTrue()
    assert_equal(true, SchemeTrue())
    assert_equal(true.to_string(), "#t")

    false = SchemeFalse()
    assert_equal(false, SchemeFalse())
    assert_equal(false.to_string(), "#f")

    assert_true(true != false)

@with_setup(setup_func)
def test_environment_find():
    env = SchemeEnvironment([SchemeSymbol('a')], [1])
    assert_equal(1, env.find(SchemeSymbol('a').value))

    assert_raises(Exception, env.find, 'foo')

@with_setup(setup_func)
def test_environment_find_complex():
    parent_env = SchemeEnvironment([SchemeSymbol('a')],[1])
    env = SchemeEnvironment([SchemeSymbol('b')], [2], parent_env)
    assert_equal(1, env.find(SchemeSymbol('a').value))
    assert_raises(Exception, env.find, SchemeSymbol('c'))

@with_setup(setup_func)
def test_enviornment_set_double():
    env = SchemeEnvironment([SchemeSymbol('a')], [1])
    assert_raises(Exception, env.set, 'a', [2])

@with_setup(setup_func)
def test_environment_update():
    root_env = SchemeEnvironment([SchemeSymbol('a')],[1])
    dict = {SchemeSymbol('a').value:2}
    root_env.update(dict)
    assert_equal(root_env.find('a'),2)
