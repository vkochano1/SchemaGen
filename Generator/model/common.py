from enum import Enum
import logging
import utils

class ObjectType(Enum):
    Message       = 2
    Field         = 3
    Enumeration   = 4
    Payload       = 6
    Configuration = 7
    Namespace     = 8
    Schema        = 9
    DataType      = 10
    SchemaOffset   = 12

class ObjectPropertyType(Enum):
    Property = 1
    Injection = 2
    VectorProperty = 3
    Attribute = 4

class PropDataCategory(Enum):
    String            = 1
    Boolean           = 2
    Enumeration       = 4
    Message           = 5
    MessageVector     = 6
    Other             = 7
    NotResolved       = 8

class ModelObject(object):
    def __init__(self, objectType, namespace, name, propDataCategory = PropDataCategory.NotResolved):
        self.__objectType = objectType
        self.logger  = logging.getLogger(self.__class__.__name__)
        self.__namespace = namespace
        self.__propDataCategory = propDataCategory
        self.name = name
        if self.__namespace != None:
            self.fullName = utils.NamespacePath.concatNamespaces(self.__namespace.fullName, self.name)
        else:
            self.fullName = self.name

    def objectType(self):
        return self.__objectType

    def namespace(self):
        return self.__namespace

    def propDataCategory(self):
        return self.__propDataCategory

    def changePropDataCategory(self, newCategory):
        self.__propDataCategory = newCategory

class ObjectProperty(object):
    def __init__(self, objectPropertyType, name, required):
        self.__objectPropertyType = objectPropertyType
        self.logger  = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.__required = required
        self.__dataType = None

    def objectPropertyType(self):
        return self.__objectPropertyType

    def required(self):
        return self.__required

    def propDataType(self):
        return self.__dataType

    def linkDataType(self, dataType):
        self.__dataType = dataType
        self.name = dataType.name


MAX_PROP_RANK = 99
