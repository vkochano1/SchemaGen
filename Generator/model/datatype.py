class DataType(object):
    def __init__(self, name, namespace, isSimpleType = True, isString = False,  enumeration = None ):
        self.includes = []
        self.additionalBaseClasses =[]
        self.specialTemplateFile = ""
        self.isSimpleType = isSimpleType
        self.name = name
        self.namespace = namespace
        self.enumeration = enumeration
        self.isString = isString
