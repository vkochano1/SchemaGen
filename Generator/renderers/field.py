import renderers.common

class Renderer(object):
    def __init__(self, schema, field):
        self.field = field
        self.schema = schema
        self.dataTypeName = field.dataType.fullName
        #prefix = renderers.common.Renderer.genQualifiedNS(field.dataType, self.field.namespace)
        #self.dataTypeName = prefix + '::' +  field.dataType.name if len(prefix) > 0 else field.dataType.name

    def genAdditionalBaseClasses(self):
        return "" if self.field.dataType.isSimpleType == True else ", public Lib::SimpleType"

    def generateEnumIncludes(self):
        if self.field.dataType.enumeration:
            out = '/'.join( self.field.dataType.namespace.components[1:])
            out = "#include<" + out + '/Enumerations/' + self.field.dataType.name + ".h>"
            return out
        return ''
