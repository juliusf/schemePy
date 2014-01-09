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
    assert_equal(str(proc), "<Procedure:test_procedure>")

@with_setup(setup_func)
def test_SchemeString():
    string = SchemeString('test_string')
    assert_equal(string.value, 'test_string')
    assert_equal(string.type, "String")
    assert_equal( str(string), '"test_string"')

@with_setup(setup_func)
def test_SchemeNumber():
    number = SchemeNumber(3)
    assert_equal(number.value, 3)
    assert_equal(number.type, "Number")
    assert_equal(str(number), '3')

@with_setup(setup_func)
def test_SchemeBoolean():
    true = SchemeTrue()
    assert_equal(true, SchemeTrue())
    assert_equal(str(true), "#t")

    false = SchemeFalse()
    assert_equal(false, SchemeFalse())
    assert_equal(str(false), "#f")

    assert_true(true != false)

@with_setup(setup_func)
def test_SchemeCons():
    cons = SchemeCons(1,2)
    assert_equal(cons.type, "SchemeCons")
    assert_equal(cons.car, 1)
    assert_equal(cons.cdr, 2)
    cons = SchemeCons( 1, SchemeCons(2, 3))
    assert_equal(str(cons), "(1 2 . 3)")
    cons = SchemeCons(1, SchemeCons(2, SchemeNil()))
    assert_equal(str(cons), "(1 2)")

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

@with_setup(setup_func)
def test_eq_operator():
    assert_equal(SchemeNumber(1), SchemeNumber(1))
