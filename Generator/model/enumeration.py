class Enumeration(object):
    def __init__(self, name, namespace, nameValueDict):
        self.name =  name
        self.nameValueDict = dict ( {(k, v.strip("''")) for k, v in nameValueDict.iteritems()} )
        self.namespace = namespace
        self.isIntEnum = True
        self.hasUnk = False

        for name, value in nameValueDict.iteritems():
            if self.isIntEnum:
                try:
                    tmp = int(value)
                except:
                    self.isIntEnum = False
            if name == "Unk":
                self.hasUnk  = True

    def __str__(self):
        items = ", ".join( [ "%s:'%s'" % (str(k), str(v)) for k, v in self.nameValueDict.iteritems()] )
        return "\n{\n enum:'%s',\n is_int:'%s',\n items:{%s}\n}\n" % (
         self.namespace.fullName + '::' + self.name, str(self.isIntEnum), items
        )
