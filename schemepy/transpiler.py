from schemepy.transpilerState import *
import re
types = {}
indentation_level = 0
functions = ""


def transpile(expression):
    global types
    types = {
        'begin': _transpile_begin,
        'internal_begin': _transpile_begin,
        'define': _transpile_define,
        'lambda': _transpile_lambda,
        '+': _transpile_plus,
        '-': _transpile_minus,
        '*': _transpile_times,
        '/': _transpile_divided,
        '<': _transpile_less,
        'if': _transpile_if
    }
    state = TranspilerState()
    program = _transpile(expression, state)
    program = re.sub(r'(?<=\S)[ ]{2,}', ' ', program)  # cleanup unneeded whitespaces
    return program


def _transpile(expression, state):
        if isinstance(expression, list):
            if isinstance(expression[0], list):
                return _transpile(expression[0], state)
            elif expression[0].value in types:
                return types[expression[0].value](expression, state)
        else:
            return state.indent() + str(expression.value)


def _transpile_begin(expression, state):
    ret = ""
    for token in expression[1:]:
        ret += "%s\n" % (_transpile(token, state))
    return state.indent() + ret


def _transpile_define(expression, state):
    if len(expression) != 3:
        raise SchemeException("Too few arguments passed to define!")
    ret = state.indent() + str(expression[1]) + " = " + str(_transpile(expression[2], state))
    return ret


def _transpile_if(expression, state):
    if not isinstance(expression, list):
        raise SchemeException("Syntax Error! if expects a list of arguments")
    if len(expression) < 3 or len(expression) > 4:
        raise SchemeException("Too few arguments passed to if. if expects at least 2 arguments. You have given me: %s" % len(expression))

    ret = state.indent() + "if "
    ret += _transpile(expression[1], state)
    ret += ":\n"
    state.push_indent()
    ret += _transpile(expression[2], state)
    state.pop_indent()
    ret += "\n"
    if len(expression) == 4:
        ret += state.indent() + "else:\n"
        state.push_indent()
        ret += _transpile(expression[3], state)
        state.pop_indent()
        ret += "\n"
    return ret


def _transpile_lambda(expression, state):
    pass


def _transpile_operator(expression, operator, state):
    ret = ""
    if len(expression) < 3:
        raise SchemeException("%s needs at least 2 parameters! You have given me: %s" %(operator, len(expression)))
    if isinstance(expression[1], list):
        ret += "( %s )" % (_transpile(expression[1], state))
    else:
        ret += "%s" % expression[1].value
    for token in expression[2:]:
        if isinstance(token, list):
            ret += " %s ( %s )" % (operator, _transpile(token, state))
        else:
            ret += " %s %s" % (operator, token.value)
    return state.indent() + ret


def _transpile_plus(expression, state):
    return _transpile_operator(expression, "+", state)


def _transpile_minus(expression, state):
    return _transpile_operator(expression, "-", state)


def _transpile_times(expression, state):
    return _transpile_operator(expression, '*', state)


def _transpile_divided(expression, state):
    return _transpile_operator(expression, '/', state)


def _transpile_less(expression, state):
    return _transpile_operator(expression, "<", state)
