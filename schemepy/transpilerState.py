from schemepy.scheme import *


class Indentation(object):
    def __init__(self, level):
        self.level = level


class TranspilerState(object):
    def __init__(self):
        self.statements = []
        self.functions = {}
        self.indentation = 0

    def _indent(self):
        self.statements.append(Indentation(self.indentation))

    def _push_indent(self):
        self.indentation += 1

    def _pop_indent(self):
        self.indentation -= 1
        if self.indentation < 0:
            raise SchemeException("Can't pop indentation_level.")