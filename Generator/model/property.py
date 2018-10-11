
class Property(object):
    isVector = False
    isInjection = False

    def __init__(self, fieldName, required, defaultValue = None):
        self.name = fieldName
        self.defaultValue = defaultValue
        self.required = required
        self.field = None
        self.message = None

    def linkField(self, field):
        self.field = field
        self.name = field.name

    def __str__(self):
        return "PROP=%s, %s " % (self.name, str(self.field))

    def __repr__(self):
            return str(self)

class InjectionProperty(object):
    isVector = False
    isInjection = True

    def __init__(self, fieldName):
        self.name = fieldName
        self.message = None
        self.field = None

    def __str__(self):
        return "INJ=%s, %s " % (self.name, str(self.field))

    def __repr__(self):
            return str(self)

class VectorProperty(object):
    isVector = True
    isInjection = False

    def __init__(self, fieldName, required):
        self.name = fieldName
        self.field = None
        self.message = None

    def linkField(self, field):
        self.field = field
        self.name = field.name

    def __str__(self):
        return "VEC=%s, %s " % (self.name, str(self.field))

    def __repr__(self):
        return str(self)
