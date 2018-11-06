import renderers.common

class Renderer(object):
    def __init__(self, schema, field):
        self.field = field
        self.schema = schema
        self.dataTypeName = field.dataType.fullName

    def genAdditionalBaseClasses(self):
        return "" if self.field.dataType.isSimpleType == True else ", public Lib::SimpleType"

    def generateDataTypeInclude(self):
        if self.field.dataType.enumeration:
            out = '/'.join( self.field.dataType.namespace().components[1:])
            out = "#include <" + out + '/Enumerations/' + self.field.dataType.name + ".h>"
            return out
        elif self.field.dataType.headerFile:
            out = """#include <{filename}>""".format(filename = self.field.dataType.headerFile)
            return out
        return ''
