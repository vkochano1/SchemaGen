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
    SchemaOffset  = 12

class ObjectPropertyType(Enum):
    Property       = 1
    Injection      = 2
    VectorProperty = 3
    Attribute      = 4

class PropDataCategory(Enum):
    String            = 1
    Boolean           = 2
    Enumeration       = 4
    Message           = 5
    MessageVector     = 6
    Other             = 7
    NotResolved       = 8

class Method(object):
    def __init__(self, name, declaration):
        self.__name = name
        self.__declaration = declaration

    def name(self): return self.__name
    def declaration(self): return self.__declaration

    def isOutOperator(self):
        return  self.__name.find("operator<<") != -1

    def isConstructorBody(self):
        return  self.__name.find("constructor_body") != -1

    def isEmptyFunction(self):
        return  self.__name.find("empty")  != -1

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

    def changeObjectType(self, newObjType):
        self.__objectType = newObjType

    def namespace(self):
        return self.__namespace

    def propDataCategory(self):
        return self.__propDataCategory

    def changePropDataCategory(self, newCategory):
        self.__propDataCategory = newCategory

    def __str__(self):
        out = """{{ Name='{name}', FullName='{fullName}', ObjectType='{objType}', PropertyType='{propType}'}}"""
        return out.format(name= self.name
                         , fullName = self.fullName
                         , objType=str(self.objectType())
                         , propType = str(self.propDataCategory()))
    def __repr__(self):
        return str(self)

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


MAX_PROP_RANK = 1
