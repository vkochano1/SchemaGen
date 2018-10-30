import logging
from common import *

class Property(ModelObject):
    def __init__(self, fieldName, required, defaultValue = None):
        super(Property, self).__init__(ObjectType.Property, None, fieldName)
        self.defaultValue = defaultValue
        self.required = required
        self.logger.debug("Created property %s" % (str(self.name)))

    def linkField(self, field):
        self.field = field
        self.name = field.name

    def __str__(self):
        return "\n{\n property:'%s',\n required='%s'\n}\n" % (str(self.field), str(self.required))

    def __repr__(self):
        return str(self)

class InjectionProperty(ModelObject):
    def __init__(self, fieldName):
        super(InjectionProperty, self).__init__(ObjectType.Injection, None, fieldName)
        self.logger.debug("Injection property %s" % (self.name))

    def __str__(self):
        return "\n{\ninjection:'%s'\n}\n" % (self.name)

    def __repr__(self):
        return str(self)

class VectorProperty(ModelObject):
    def __init__(self, fieldName, required):
        super(VectorProperty, self).__init__(ObjectType.VectorProperty, None, fieldName)
        self.required = required
        self.logger.debug("Created vector of %s" %(self.name))

    def linkField(self, field):
        self.field = field
        self.name = field.name

    def __str__(self):
        return "\n{ vector:'%s'\n }\n" % (self.field)

    def __repr__(self):
        return str(self)
