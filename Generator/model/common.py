from enum import Enum
import logging
import utils

class ObjectType(Enum):
    Property      = 1
    Message       = 2
    Field         = 3
    Enumeration   = 4
    Injection     = 5
    Payload       = 6
    Configuration = 7
    Namespace     = 8
    Schema        = 9
    DataType      = 10
    VectorProperty  = 11


class FieldDataCategory(Enum):
    String            = 1
    Boolean           = 2
    CharEnumeration   = 3
    IntEnumeration    = 4
    Messsage          = 5
    MessageVector     = 6
    Other             = 7


class ModelObject(object):
    def __init__(self, objectType, namespace, name):
        self.__objectType = objectType
        self.logger  = logging.getLogger(self.__class__.__name__)
        self.namespace = namespace
        self.name = name
        if namespace != None:
            self.fullName = utils.NamespacePath.concatNamespaces(namespace.fullName, self.name)
        else:
            self.fullName = self.name

    def objectType(self):
        return self.__objectType
