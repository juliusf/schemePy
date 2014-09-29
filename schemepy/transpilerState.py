from schemepy.scheme import *


class TranspilerState(object):
    def __init__(self):
        self.functions = {}
        self.indentation = 0

    def indent(self):
        return ' ' * 4 * self.indentation

    def push_indent(self):
        self.indentation += 1

    def pop_indent(self):
        self.indentation -= 1
        if self.indentation < 0:
            raise SchemeException("Can't pop indentation_level.")
