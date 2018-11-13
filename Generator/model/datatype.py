from common import *

class DataType(ModelObject):
    def __init__(self, name, namespace
                , isSimpleType = False
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
            self.changePropDataCategory(PropDataCategory.Enumeration)
        elif isString == True:
            self.changePropDataCategory(PropDataCategory.String)
        elif name == "Flag" or name == "Boolean":
            self.changePropDataCategory(PropDataCategory.Boolean)
        else:
            self.changePropDataCategory(PropDataCategory.Other)

        self.logger.debug("Created data type {name} ({category})".format(name = self.name, category =str(self.propDataCategory())) )
