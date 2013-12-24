from schemepy.scheme import *
def _tokenize(input):
    """Tokenizes a given input string"""
    return input.replace("(","( ").replace(")", " )").split()

def _buildValue(value):
    if value == '#t':
        return SchemeTrue()
    elif value == '#f':
        return SchemFalse()
    elif value == "'()":
        return SchemeNil()
    else:
        try:
            return SchemeNumber(int(value))
        except ValueError:
            try:
                return SchemeNumber(float(value))
            except ValueError:
                return SchemeSymbol(value)

def _parse_tokens(tokens):
    """generates executable syntax expression from a list of tokens"""
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        values = []
        while tokens[0] != ')':
            values.append(_parse_tokens(tokens))
        tokens.pop(0)
        return values
    elif token == "\'(":    #TODO: Quotes
        values = []
        while tokens[0] != ')':
            values.append(_parse_tokens(tokens))
        tokens.pop(0)
        return values
    else:
        return(_buildValue(token))

def parse(input):
    """converts a string to a executable syntax expression"""
    return _parse_tokens(_tokenize(input))

def to_string(expression):
    if isinstance(expression, list):
        return _to_string_list(expression)
    else:
        return _to_string_expression(expression)

def _to_string_list(list):
    result = "("
    for expr in list:
        result += to_string(expr) + " "
    return result.strip() + ")"

def _to_string_expression(expr):
    return str(expr)
