from schemepy.scheme import *
from functools import reduce

builtin_functions = dict()

builtin_functions["+"] = SchemeProcedure("+", lambda *args: reduce(lambda x, y: SchemeNumber(x.value+y.value), args) )

root_enviornment = Enviornment() 
root_enviornment.update(builtin_functions)

def evaluate(expression, enviornment=root_enviornment):
	"""Evaluates an executable expression"""
	if isinstance(expression, list):
		syntax = {}
		
		if expression[0].value in syntax: #check whether the first element is syntax
			syntax[expression[0]]()
		else:						#else: run procedure
			exps = [evaluate(exp, enviornment) for exp in expression]
			procedure = exps.pop(0)
			return procedure.impl(*exps)
	elif expression.type == "Symbol":
		return enviornment.find(expression.value)
	else:
		return expression

