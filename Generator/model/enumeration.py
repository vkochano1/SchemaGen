import utils
from common import *

class Enumeration(ModelObject):
    def __init__(self, name, namespace, nameValueArr, storageType = None):
        super(Enumeration, self).__init__(ObjectType.Enumeration, namespace, name)
        self.nameValueArr = nameValueArr
        self.isIntEnum = True
        self.hasUnk = False
        self.storageType = storageType
        self.hasCustomStreamOut = None
        self.methods = []
        self.headerFile = self.fullName.replace("::","/")
        self.rank = MAX_PROP_RANK

        for name, value in nameValueArr:
            if self.isIntEnum:
                try:
                    tmp = int(value)
                except:
                    self.isIntEnum = False
            if name == "Unk":
                self.hasUnk  = True

        if self.hasUnk == False:
            self.nameValueArr.insert(0, ('Unk',-99999) if self.isIntEnum else ('Unk',"'?'") )

        self.nameValueDict = dict (self.nameValueArr)
        self.valCount = len(self.nameValueDict)

    def addMethod(self, method):
        if method [0] == 'operator<<':
            self.hasCustomStreamOut = True
        self.methods.append(method)

    def __str__(self):
        items = ", ".join( [ "%s:'%s'" % (str(k), str(v)) for k, v in self.nameValueDict.iteritems()] )
        return "\n{\n enum:'%s',\n is_int:'%s',\n items:{%s}\n}\n" % (
         self.fullName, str(self.isIntEnum), items
        )
