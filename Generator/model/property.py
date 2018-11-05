import logging
from common import *

class Property(ObjectProperty):
    def __init__(self, fieldName, required, defaultValue = None):
        super(Property, self).__init__(ObjectPropertyType.Property, fieldName, required)
        self.defaultValue = defaultValue
        self.logger.debug("Created property %s" % (str(self.name)))

    def __str__(self):
        return "\n{\n property:'%s',\n required='%s'\n}\n" % (str(self.field), str(self.required()))

    def __repr__(self):
        return str(self)

class InjectionProperty(ObjectProperty):
    def __init__(self, fieldName):
        super(InjectionProperty, self).__init__(ObjectPropertyType.Injection, fieldName, True)
        self.logger.debug("Injection property %s" % (self.name))

    def __str__(self):
        return "\n{\ninjection:'%s'\n}\n" % (self.name)

    def __repr__(self):
        return str(self)

class VectorProperty(ObjectProperty):
    def __init__(self, fieldName):
        super(VectorProperty, self).__init__(ObjectPropertyType.VectorProperty, fieldName, True)
        self.logger.debug("Created vector of %s" %(self.name))

    def __str__(self):
        return "\n{ vector:'%s'\n }\n" % (self.field)

    def __repr__(self):
        return str(self)
