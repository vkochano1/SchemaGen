from common import *

class DataType(ModelObject):
    def __init__(self, name, namespace, isSimpleType = True, isString = False,  enumeration = None, headerFile = None ):
        super(DataType, self).__init__(ObjectType.DataType, namespace, name)
        self.includes = []
        self.isSimpleType = isSimpleType
        self.enumeration = enumeration
        self.isString = isString
        self.headerFile = headerFile
        self.isBoolean = (name == "Flag" or name == "Boolean")
