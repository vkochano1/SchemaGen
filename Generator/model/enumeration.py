class Enumeration(object):
    def __init__(self, name, namespace, nameValueDict):
        self.name =  name
        self.nameValueDict = nameValueDict
        self.namespace = namespace

        self.isIntEnum = True
        self.isCharEnum = True
        self.hasUnk = False
        for name, value in nameValueDict.iteritems():
            if self.isIntEnum:
                try:
                    tmp = int(value)
                except:
                    self.isIntEnum = False
            if self.isCharEnum:
                self.isCharEnum = (value[0] == "\'" and value[-1] == "\'" and len(value) == 3)

            if name == "Unk":
                self.hasUnk  = True


    def __str__(self):
        return self.namespace.fullName + '::' + self.name
