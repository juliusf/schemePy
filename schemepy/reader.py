from schemepy.scheme import *
from schemepy.stream import Stream

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


def parse(inp):
    if not (inp.isspace() or inp == ""):
        stream = Stream(inp)
        return _parse_helper(stream)
    else:
        raise SchemeException("Unexpected EOF!")


def _parse_helper(stream):
    while(not stream.is_EOF()):
        stream.skip_whitespace()
        c = stream.peek()

        if c == '(':
            return parse_list(stream)

        elif c == '+' or c == '-' or (c >= '0' and c<= '9'):
            return parse_number(stream)

        elif c == '"':
            return parse_string(stream)
        elif c == "'":
            return parse_quote(stream)
        elif c == "#":
            return parse_boolean(stream)
        elif c == ";":
            parse_comment(stream)
        else:
            return parse_symbol(stream)

def parse_list(stream):
    l = []
    stream.skip(1) #skip (
    stream.skip_whitespace()
    while stream.is_EOF() == False and stream.peek() != ')':
        l.append(_parse_helper(stream))
        stream.skip_whitespace()
    if stream.is_EOF():
        raise SchemeException("Missing )!")
    if not stream.is_EOF(1): #true for the last input
        stream.skip(1) #skip )
    return l

def parse_number(stream):
    c = stream.read_until_whitespace()
    if len(c) == 1 and (c == "+" or c == "-"):
        return SchemeSymbol(c)
    else:
        try:
            return SchemeNumber(int(c))
        except ValueError:
            try:
                return SchemeNumber(float(c))
            except ValueError:
                raise SchemeException('%s is a malformed number!' % (c) )

def parse_string(stream):
    stream.skip(1)
    def cond(arg):
        if arg == '"':
            return False
        else:
            return True
    string = stream.read_until( cond )
    stream.skip(1) # consume closing "
    return SchemeString(string)

def parse_quote(stream):
    stream.skip(1) #consume ;
    return [SchemeSymbol('quote'), _parse_helper(stream)]

def parse_symbol(stream):
    return SchemeSymbol(stream.read_until_whitespace())

def parse_boolean(stream):
    stream.skip(1)
    c = stream.read_until_whitespace()
    if c == "t" or c == "false":
        return SchemeTrue()
    elif c =="f" or c == "false":
        return SchemeFalse()
    else:
        SchemeException(" %s is no valid SchemeBoolean!" % (c))

def parse_comment(stream):
    def cond(arg):
        if arg == '\n':
            return False
        else:
            return True
    stream.read_until( cond )


