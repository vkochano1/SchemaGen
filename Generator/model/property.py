import logging

class Property(object):
    isVector = False
    isInjection = False

    def __init__(self, fieldName, required, defaultValue = None):
        self.logger = logging.getLogger(__name__)
        self.name = fieldName
        self.defaultValue = defaultValue
        self.required = required
        self.field = None
        self.message = None
        self.logger.debug("Created property %s" % (str(self.name)))

    def linkField(self, field):
        self.field = field
        self.name = field.name

    def __str__(self):
        return "\n{\n property:'%s',\n required='%s'\n}\n" % (str(self.field), str(self.required))

    def __repr__(self):
            return str(self)

class InjectionProperty(object):
    isVector = False
    isInjection = True

    def __init__(self, fieldName):
        self.logger = logging.getLogger(__name__)
        self.name = fieldName
        self.message = None
        self.field = None
        self.logger.debug("Injection property %s" % (self.name))

    def __str__(self):
        return "\n{\ninjection:'%s'\n}\n" % (self.name)

    def __repr__(self):
            return str(self)

class VectorProperty(object):
    isVector = True
    isInjection = False

    def __init__(self, fieldName, required):
        self.logger = logging.getLogger(__name__)
        self.name = fieldName
        self.field = None
        self.message = None
        self.required = required
        self.logger.debug("Created vector of %s" %(self.name))

    def linkField(self, field):
        self.field = field
        self.name = field.name

    def __str__(self):
        return "\n{ vector:'%s'\n }\n" % (self.field)

    def __repr__(self):
        return str(self)
