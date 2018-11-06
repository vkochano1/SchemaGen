from common import *

class DataType(ModelObject):
    def __init__(self, name, namespace
                , isSimpleType = True
                , isString = False
                , enumeration = None
                , headerFile = None
                , rank = MAX_PROP_RANK ):
        super(DataType, self).__init__(ObjectType.DataType, namespace, name)
        self.isSimpleType = isSimpleType
        self.enumeration = enumeration
        self.headerFile = headerFile
        if self.headerFile == None:
            if enumeration != None:
                self.headerFile = enumeration.namespace().fullName.replace("::", "/") + "/" + enumeration.name + ".h"
            else:
                self.headerFile = self.namespace().fullName.replace("::", "/") + "/" + name + ".h"
        self.rank = rank

        if enumeration != None:
            self.__propDataCategory = PropDataCategory.Enumeration
        elif isString == True:
            self.__propDataCategory = PropDataCategory.String
        elif name == "Flag" or name == "Boolean":
            self.__propDataCategory = PropDataCategory.Boolean

        self.logger.debug("Created data type {name}".format(name = self.name) )
