from schemepy.scheme import *
from functools import reduce

builtin_functions = dict()

builtin_functions["+"] = SchemeProcedure("+", lambda *args: reduce(lambda x, y: SchemeNumber(x.value+y.value), args) )

root_environment = environment() 
root_environment.update(builtin_functions)

def evaluate(expression, environment=root_environment):
    """Evaluates an executable expression"""
    if isinstance(expression, list):
        syntax = {'define':_syntax_define, 'begin':_syntax_begin}
        
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
    expressions = expression[1:]
    exps = [evaluate(exp, environment) for exp in expressions]
    return exps[-1] #returns the last result of the begin statement

def _syntax_define(expression, environment):
    var, expr = expression[1], expression[2:]
    if isinstance(var, list): #shorthand lambda syntax
        pass # TODO: IMPLEMENT
    else:
        environment.set(var.value, evaluate(expr[0], environment))
