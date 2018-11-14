import logging
from common import *

class Attribute(ObjectProperty):
    def __init__(self, name, constValue):
        super(Attribute, self).__init__(ObjectPropertyType.Attribute, name, True)
        self.constValue = constValue
        self.logger.debug("Created Attribute %s" % (str(self.name)))

    def __str__(self):
        return """{{ Attribute:'{name}', ConstValue='{constValue}' }}""".format( name = str(self.name), required = str(self.constValue))

    def __repr__(self): return str(self)

class Property(ObjectProperty):
    def __init__(self, fieldName, required, defaultValue = None):
        super(Property, self).__init__(ObjectPropertyType.Property, fieldName, required)
        self.defaultValue = defaultValue
        self.logger.debug("Created property %s" % (str(self.name)))

    def __str__(self):
        return """{{ Property:'{name}', Required='{required}' }}""".format( name = str(self.name), required = str(self.required()))

    def __repr__(self): return str(self)

class InjectionProperty(ObjectProperty):
    def __init__(self, fieldName):
        super(InjectionProperty, self).__init__(ObjectPropertyType.Injection, fieldName, True)
        self.logger.debug("Injection property %s" % (self.name))

    def __str__(self):
        return """{{ Injection: '{name}' }}""".format(name = self.name)

    def __repr__(self): return str(self)

class VectorProperty(ObjectProperty):
    def __init__(self, fieldName):
        super(VectorProperty, self).__init__(ObjectPropertyType.VectorProperty, fieldName, True)
        self.logger.debug("Created vector of %s" %(self.name))

    def __str__(self):
        return """{{ Vector: '{name}' }}""".format(name = self.name)

    def __repr__(self): return str(self)
