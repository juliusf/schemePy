from schemepy.scheme import *

types = {}
indentation_level = 0


def transpile(expression):
    global types
    types = {
        'begin': _transpile_begin,
        'internal_begin': _transpile_begin,
        'define': _transpile_define,
        '+': _transpile_plus,
        '-': _transpile_minus,
        '*': _transpile_times,
        '/': _transpile_divided,
        '<': _transpile_less,
        'if': _transpile_if
    }

    return _transpile(expression)


def _indent():
    return indentation_level * 4 * " "


def _push_indent():
    global indentation_level
    indentation_level += 1


def _pop_indent():
    global indentation_level
    indentation_level -= 1
    if indentation_level < 0:
        raise SchemeException("Can't pop indentation_level.")


def _transpile(expression):
        if isinstance(expression, list):
            if isinstance(expression[0], list):
                return _transpile(expression[0])
            elif expression[0].value in types:
                return types[expression[0].value](expression)
        else:
            return expression.value


def _transpile_begin(expression):
    ret = ""
    for token in expression[1:]:
        ret += "%s\n" % (_transpile(token))
    return _indent() + ret


def _transpile_define(expression):
    pass


def _transpile_if(expression):
    if not isinstance(expression, list):
        raise SchemeException("Syntax Error! if expects a list of arguments")
    if len(expression) < 3 or len(expression) > 4:
        raise SchemeException("Two few arguments passed to if. if expects at least 2 arguments. You have given me: %s" % len(expression))

    ret = _indent() + "if "
    ret += _transpile(expression[1])
    ret += ":\n"
    _push_indent()
    ret += _indent() + _transpile(expression[2])
    _pop_indent()
    ret += "\n"
    if len(expression) == 4:
        ret += _indent() + "else:\n"
        _push_indent()
        ret += _indent() + _transpile(expression[3])
        _pop_indent()
        ret += "\n"
    return ret


def _transpile_operator(expression, operator):
    ret = ""
    if len(expression) < 3:
        raise SchemeException("%s needs at least 2 parameters! You have given me: %s" %(operator, len(expression)))
    if isinstance(expression[1], list):
        ret += "( %s )" % (_transpile(expression[1]))
    else:
        ret += "%s" % expression[1].value
    for token in expression[2:]:
        if isinstance(token, list):
            ret += " %s ( %s )" % (operator, _transpile(token))
        else:
            ret += " %s %s" % (operator, token.value)
    return _indent() + ret


def _transpile_plus(expression):
    return _transpile_operator(expression, "+")


def _transpile_minus(expression):
    return _transpile_operator(expression, "-")


def _transpile_times(expression,):
    return _transpile_operator(expression, '*')


def _transpile_divided(expression):
    return _transpile_operator(expression, '/')


def _transpile_less(expression):
    return _transpile_operator(expression, "<")
