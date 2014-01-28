from schemepy.scheme import *

types = {}

def transpile(expression):
    global types
    types = {
        'begin': _transpile_begin,
        'internal_begin' : _transpile_begin,
        'define':_transpile_define,
        '+':_transpile_plus
    }
    return _transpile(expression)

def _transpile(expression):
        if isinstance(expression, list):
            if isinstance(expression[0], list):
                return _transpile(expression[0])
            elif expression[0].value in types:
                return  types[expression[0].value](expression)
        else:
            return expression.value

def _transpile_begin(expresison):
    ret = ""
    for token in expresison[1:]:
        ret += "%s\n" % (_transpile(token))
    return ret

def _transpile_define(expression):
    pass
def _transpile_operator(expression, operator):
    ret = ""
    if len(expression) < 3:
        raise SchemeException("%s needs at least 2 parameters! You have given me: %s" %(operator, len(expression)))
    if isinstance(expression[1], list):
        ret += "( %s )" % (_transpile(expression[1]))
    else:
        ret += "%s" % (expression[1].value)
    for token in expression[2:]:
        if isinstance(token, list):
            ret +=  " %s ( %s )" % (operator, _transpile(token))
        else:
            ret += " %s %s" % (operator, token.value)
    return ret

def _transpile_plus(expression):
    return _transpile_operator(expression, "+")




