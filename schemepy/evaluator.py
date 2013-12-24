from schemepy.scheme import *
from functools import reduce

builtin_functions = dict()

builtin_functions["+"] = SchemeProcedure("+", lambda *args: reduce(lambda x, y: SchemeNumber(x.value+y.value), args) )
builtin_functions["="] = SchemeProcedure("=", lambda *args: reduce(lambda x ,y: SchemeTrue() if (x== SchemeTrue() and y== SchemeTrue() ) else SchemeFalse(), map(lambda x: SchemeFalse() if x != args[0] else SchemeTrue(), args[1:])))


root_environment = SchemeEnvironment()
root_environment.update(builtin_functions)

def reset_enviornment():
    global root_environment
    root_environment =  SchemeEnvironment()
    root_environment.update(builtin_functions)

def evaluate(expression, environment=root_environment):
    """Evaluates an executable expression"""
    if isinstance(expression, list):
        syntax = {'define':_syntax_define, 'begin':_syntax_begin, 'lambda':_syntax_lambda, 'if':_syntax_if}
        if expression[0].value in syntax: #check whether the first element is syntax
            return syntax[expression[0].value](expression, environment)    #call syntax handler
        else:                        #else: run procedure
            exps = [evaluate(exp, environment) for exp in expression] #recursively call evaluate for every exp in expression
            procedure = exps.pop(0) #get SchemeProcedure object
            return procedure.impl(*exps) # call procedure with params
    elif expression.type == "Symbol":    #if it's a symbol, lookup in environment
        return environment.find(expression.value)
    else:
        return expression    #schemeNumber

def _syntax_begin(expression, environment):
    expressions = expression[1:] #maybe [1:]?
    exps = [evaluate(exp, environment) for exp in expressions]
    return exps[-1] #returns the last result of the begin statement

def _syntax_define(expression, environment):
    var, expr = expression[1], expression[2:]
    if isinstance(var, list): #shorthand lambda syntax
        pass # TODO: IMPLEMENT
    else:
        environment.set(var.value, evaluate(expr[0], environment))

def _syntax_lambda(expression, environment):
    vars, expr = expression[1], expression[2]
    return SchemeProcedure('lambda', lambda *args : evaluate(expr, SchemeEnvironment(vars, args, environment)) )

def _syntax_if(expression, environment):
    if len(expression) != 4:
        raise SchemeException("if: invalid syntax. if expects exactly 3 arguments: if <condition> <truePath> <falsePath>")
    condition, true_path, false_path = expression[1], expression[2], expression[3]
    return evaluate(true_path, environment) if evaluate(condition, environment) == SchemeTrue() else evaluate(false_path, environment)