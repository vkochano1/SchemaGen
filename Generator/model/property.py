
class Property(object):
    def __init__(self, message, fieldName, required, defaultValue = None):
        self.name = fieldName
        self.defaultValue = defaultValue
        self.required = required
        self.field = None
        self.message = message

    def linkField(self, field):
        self.field = field
        self.name = field.name

    def __str__(self):
        return "PROP=%s, %s " % (self.name, str(self.field))

    def __repr__(self):
            return str(self)
