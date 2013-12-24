class SchemeType:
    def __eq__(a, b):
        if not ( isinstance(a, SchemeType) and isinstance(b, SchemeType)):
            return False
        elif a.type != b.type:
            return False
        elif a.value != b.value:
            return False
        else:
            return True
    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.value)

class SchemeProcedure(SchemeType):
    def __init__(self, name, impl):
        self.name = name
        self.impl = impl
        self.type = "Procedure"
    def __str__(self):
        return '<Procedure:%s>' % self.name
    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.name)

class SchemeString:
    def __init__(self, value):
        self.value = value
        self.type = 'String'
    def __str__(self):
        return '"%s"' % (self.value)

class SchemeNumber(SchemeType):
    def __init__(self, value):
        self.value = value
        self.type = 'Number'
    def impl(self, *args):
        return self.value
    def __str__(self):
        return '%s' % (self.value)

class SchemeSymbol(SchemeType):
    def __init__(self, value):
        self.value = value
        self.type = 'Symbol'
    def __str__(self):
        return '%s' % (self.value)

class SchemeTrue(SchemeType):
    def __init__(self):
        self.type = "SchemeTrue"
        self.value = "True"
    def __str__(self):
        return '#t'


class SchemeFalse(SchemeType):
    def __init__(self):
        self.type = "SchemeFalse"
        self.value = "False"
    def __str__(self):
        return '#f'

class SchemeCons(SchemeType):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
        self.type = "SchemeCons"
    def __str__(self):
        return "(%s . %s)" % (self.car, self.cdr)
    def __eq__(a, b):
        if not ( isinstance(a, SchemeCons) and isinstance(b, SchemeCons)):
            return False
        elif a.car != b.car or a.cdr != b.cdr:
            return False
        else:
            return True
    def __repr__(self):
        return "<SchemeCons: (%s.%s)>" % (self.car.to_string(), self.cdr.to_string())

class SchemeException(Exception):
    pass

class SchemeEnvironment:
    def __init__(self, params = None, args = None , parentEnv=None):
        self.parentEnv = parentEnv
        self._dict = {}
        values = []
        if params != None and args != None:
            [values.append(vals.value) for vals in params] ##hacky
            self._dict = dict(zip(values, args))

    def find(self, key):
        val = self._dict.get(key)
        if val != None:
            return val
        else:
            if self.parentEnv != None:
                return self.parentEnv.find(key)
            else:
                raise SchemeException("Undefined Symbol %s!" % (key))

    def update(self, dict):
        for key  in dict.keys():
            self._dict[key] = dict[key]

    def set(self, key, value):
        if key in self._dict:
            raise SchemeException("%s has already been defined. Use set! to redefine" % (key) )
        else:
            self._dict[key]=value

