from schemepy.scheme import *
from functools import reduce
import sys

builtin_functions = dict()


builtin_functions["+"] = SchemeProcedure("+", lambda *args: reduce(lambda x, y: SchemeNumber(x.value+y.value), args) )
builtin_functions["-"] = SchemeProcedure("-", lambda *args: reduce(lambda x, y: SchemeNumber(x.value-y.value), args) )
builtin_functions["*"] = SchemeProcedure("*", lambda *args: reduce(lambda x, y: SchemeNumber(x.value*y.value), args) )
builtin_functions["/"] = SchemeProcedure("/", lambda *args: reduce(lambda x, y: SchemeNumber(x.value/y.value), args) )

builtin_functions["="] = SchemeProcedure("=", lambda *args: reduce(lambda x, y: SchemeTrue() if (x == SchemeTrue() and y == SchemeTrue() ) else SchemeFalse(), map(lambda x: SchemeFalse() if x != args[0] else SchemeTrue(), args[1:])))
builtin_functions[">"] = SchemeProcedure(">", lambda *args: SchemeTrue() if reduce(lambda x, y: x + y , map(lambda x: 1 if args[x].value > args[x + 1].value else 0, range(len(args) -1))) == len(args)-1 else SchemeFalse())
builtin_functions[">="] = SchemeProcedure(">=", lambda *args: SchemeTrue() if reduce(lambda x, y: x + y , map(lambda x: 1 if args[x].value >= args[x + 1].value else 0, range(len(args) -1))) == len(args)-1 else SchemeFalse())
builtin_functions["<"] = SchemeProcedure("<", lambda *args: SchemeTrue() if reduce(lambda x, y: x + y , map(lambda x: 1 if args[x].value < args[x + 1].value else 0, range(len(args) -1))) == len(args)-1 else SchemeFalse())
builtin_functions["<="] = SchemeProcedure("<=", lambda *args: SchemeTrue() if reduce(lambda x, y: x + y , map(lambda x: 1 if args[x].value <= args[x + 1].value else 0, range(len(args) -1))) == len(args)-1 else SchemeFalse())

builtin_functions["and"] = SchemeProcedure("and", lambda *args: _make_scheme_bool( SchemeFalse() not in args ))
builtin_functions["or"] = SchemeProcedure("or", lambda *args: _make_scheme_bool( SchemeTrue() in args ))
builtin_functions["not"] = SchemeProcedure("not", lambda *args: _make_scheme_bool( args[0] == SchemeFalse() ))

root_environment = SchemeRootEnviornment()
root_environment.update(builtin_functions)


def evaluate(expression, environment=root_environment):
    """Evaluates an executable expression"""
    if isinstance(expression, list):
        if len(expression) == 0:
            raise SchemeException("Syntax Error!")

        to_execute = expression[0]
        syntax = {
            'define':_syntax_define,
            'begin':_syntax_begin,
            'lambda':_syntax_lambda,
            'if':_syntax_if,
            'cons':_syntax_cons,
            'car':_syntax_car,
            'cdr':_syntax_cdr,
            'let':_syntax_let,
            'set!':_syntax_set,
            'quote': _syntax_quote,
            'exit': _syntax_exit
        }
        if isinstance(expression[0], list):
            to_execute = evaluate(expression[0], environment)


        if isinstance(to_execute, SchemeSymbol) and to_execute.value in syntax: #check whether the first element is syntax
            return syntax[to_execute.value](expression, environment)    #call syntax handler
        else:                        #else: run procedure
            exps = [evaluate(exp, environment) for exp in expression[1:]] #recursively call evaluate for every exp in expression
            procedure = evaluate(to_execute, environment) #get SchemeProcedure object
            if isinstance(procedure, SchemeProcedure):
                return procedure.impl(*exps) # call procedure with params
            else:
                raise SchemeException("%s is not a procedure" % (procedure))
    elif expression.type == "Symbol":    #if it's a symbol, lookup in environment
        return environment.find(expression.value)
    else:
        return expression    #schemeNumber

def _syntax_begin(expression, environment):
    if len(expression) < 2:
        raise SchemeException("begin requires at least one argument!")
    expressions = expression[1:]
    exps = [evaluate(exp, environment) for exp in expressions]
    return exps[-1] #returns the last result of the begin statement

def _syntax_define(expression, environment):
    if len(expression) != 3:
        raise SchemeException("define: define expects exactly 2 arguments: define <variable> <value>. Got %s instead" % (expression))
    var, expr = expression[1], expression[2:]
    if isinstance(var, list): #shorthand lambda syntax
        var = expression[1][0]
        expression[1] = expression[1][1:]
        l = _syntax_lambda(expression, environment)
        environment.set(var.value, l)
    else:
        environment.set(var.value, evaluate(expr[0], environment))

def _syntax_set(expression, environment):
    if len(expression) != 3:
        raise SchemeException("set: set expects exactly 2 arguments: define <variable> <value>.")
    var, expr = expression[1], expression[2:]
    environment.set_overwrite(var.value, evaluate(expr[0], environment))


def _syntax_lambda(expression, environment):
    if len(expression) != 3:
        raise SchemeException("lambda: lambda expects exactly to 2 arguments: lambda <variables> <implementation>")
    vars, expr = expression[1], expression[2]
    return SchemeProcedure('lambda', lambda *args : evaluate(expr, SchemeEnvironment(vars, args, environment)) )

def _syntax_if(expression, environment):
    if len(expression) != 4:
        raise SchemeException("if: if expects exactly 3 arguments: if <condition> <truePath> <falsePath>")
    condition, true_path, false_path = expression[1], expression[2], expression[3]
    return evaluate(true_path, environment) if evaluate(condition, environment) == SchemeTrue() else evaluate(false_path, environment)

def _syntax_cons(expression, environment):
    if len (expression) != 3:
        raise SchemeException("cons: cons expects exactly 2 arguments: cons <car> <cdr>")
    car, cdr = expression[1], expression[2]
    return SchemeCons(evaluate(car, environment), evaluate(cdr, environment))

def _syntax_car(expression, enviornment):
    if len (expression) != 2:
        raise SchemeException("car: car expects exactly 2 arguments: car <cons>")
    cons = evaluate(expression[1], enviornment)
    print(expression)
    if not isinstance(cons, SchemeCons):
        raise SchemeException("car: car expects a SchemeCons as first parameter. Got a %s instead." % (cons))
    return evaluate(cons.car, enviornment)

def _syntax_cdr(expression, enviornment):
    if len (expression) != 2:
        raise SchemeException("cdr: cdr expects exactly 2 arguments: cdr <cons>")
    cons = evaluate(expression[1], enviornment)
    if not isinstance(cons, SchemeCons):
        raise SchemeException("cdr: cdr expects a SchemeCons as first parameter. Got a %s instead." % (cons))
    return evaluate(cons.cdr, enviornment)

def _syntax_let(expression, enviornment):
    if len(expression) != 3:
        raise SchemeException("let: let expects exactly two parameters: let <variable definitions> <implementation>")
    defs, impl = expression[1], expression[2]
    newEnv = SchemeEnvironment(None, None, enviornment)
    for expr in defs:
        newEnv.set(expr[0].value, expr[1])
    return evaluate(impl, newEnv)

def _syntax_quote(expression, enviornment):
    if len(expression) != 2:
        raise SchemeException("quote expects exactly one argument")

    return SchemeNil() if isinstance(expression[1], list) and len(expression[1]) == 0 else expression[1]

def _syntax_exit(expression, enviornment):
    sys.exit(0)
def _make_scheme_bool(cond):
    return SchemeTrue() if cond else SchemeFalse()

