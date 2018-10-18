import utils

class Enumeration(object):
    def __init__(self, name, namespace, nameValueArr, storageType = None):
        self.name =  name
        self.nameValueArr = nameValueArr
        self.namespace = namespace
        self.isIntEnum = True
        self.hasUnk = False
        self.storageType = storageType
        self.fullName = utils.NamespacePath.concatNamespaces(namespace.fullName, self.name)
        self.hasCustomStreamOut = None
        self.methods = []

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
        if method [0] == 'operator <<':
            self.hasCustomStreamOut = True
        self.methods.append(method)

    def __str__(self):
        items = ", ".join( [ "%s:'%s'" % (str(k), str(v)) for k, v in self.nameValueDict.iteritems()] )
        return "\n{\n enum:'%s',\n is_int:'%s',\n items:{%s}\n}\n" % (
         self.namespace.fullName + '::' + self.name, str(self.isIntEnum), items
        )
