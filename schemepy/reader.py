from schemepy.scheme import *
import re


def _tokenize(input):
    """Tokenizes a given input string"""
    tokens = input.replace("("," ( ").replace(")", " ) ")
    tokens = re.split('("[^"]+"|[^"\s]+)', tokens)
    tokens = list( filter(lambda i: not ( re.search('^\s*$',i) or i == '') , tokens) )
    if len(tokens) == 3:
        raise SchemeException("Unexpected EOF")

    return tokens



def _buildValue(value):
    if value == '#t':
        return SchemeTrue()
    elif value == '#f':
        return SchemeFalse()
    else:
        try:
            return SchemeNumber(int(value))
        except ValueError:
            try:
                return SchemeNumber(float(value))
            except ValueError:
                if(value[0] == '"'):
                    return SchemeString(value[1:-1])
                else:
                    return SchemeSymbol(value)

def _parse_tokens(tokens):
    """generates executable syntax expression from a list of tokens"""
    if len(tokens) == 0:
        raise SchemeException("Unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        values = []
        while len(tokens) > 0 and tokens[0] != ')':
            values.append(_parse_tokens(tokens))
        if len(tokens) == 0:
            raise SchemeException("Unexpected EOF")
        tokens.pop(0)
        return values
    else:
        return(_buildValue(token))

def parse(input):
    """converts a string to a executable syntax expression"""
    return _parse_tokens(_tokenize(_preprocess(input)))

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

def _preprocess(inp):
    inp = re.sub(r";+.+\n|\n|\r|\t", " ", inp) #remove quotes, new lines, whitespaces and tabs
    inp = re.sub("'(\(.*\))", r"(quote \1)", inp) #replace '(%foo) with (quote (foo))
    inp = re.sub("'([^\s]*)", r"(quote \1)", inp) # replace 'foo with (quote foo)
    return "(internal_begin " + inp + ")" #implicit multiline evaluation


def parse_new(stream):
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
        else:
            return parse_symbol(stream)

def parse_list(stream):
    l = []
    stream.skip(1) #skip (
    stream.skip_whitespace()
    while stream.is_EOF() == False and stream.peek() != ')':
        l.append(parse_new(stream))
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
    def cond(arg, s):
        if arg == '"':
            return False
        else:
            return True
    return SchemeString(stream.read_unitil_cond( cond ))


def parse_quote(stream):
    stream.skip(1)
    return [SchemeSymbol('quote'), parse_new(stream)]

def parse_symbol(stream):
    return SchemeSymbol(stream.read_until_whitespace)


