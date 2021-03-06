import model.namespace
import renderers.common
from  model.common import *

class Renderer:
    def __init__(self, model, message):
        self.model = model
        self.message = message
        self.propMaxLen = 0
        self.hasMessageVectorProp = False
        self.countPropsRequired = 0
        self.constructorBody = None
        self.hasCustomEmptyMethod = False

        def weight(prop):
            if prop.propDataType().objectType() == ObjectType.Field:
                return prop.propDataType().dataType.rank
            else :
                return MAX_PROP_RANK

        self.sortedProps = sorted(self.message.props, key = weight)
        self.countPropsAll = len(self.message.props)

        for method in self.message.methods:
            if method.isConstructorBody():
                self.constructorBody = method.declaration()
            elif method.isEmptyFunction():
                self.hasCustomEmptyMethod = True

        for prop in self.message.props:
            self.propMaxLen = max(self.propMaxLen, len(self.genPropType(prop)))
            self.hasMessageVectorProp = self.hasMessageVectorProp or (
            prop.propDataType().objectType() == ObjectType.Message and prop.propDataType().isVector)
            if prop.required() == True:
                self.countPropsRequired = self.countPropsRequired + 1
    @staticmethod
    def generateInclDirForNamespace( obj):
        return  '/'.join( obj.namespace().components[1:])

    def genRightPaddedName(self, name):
        return name + ' ' * (self.propMaxLen - len(name))

    def quoteVal(self, prop):
        if prop.propDataType().dataType.propDataCategory() == PropDataCategory.String and (
            prop.defaultValue.find("::") == -1 and  prop.defaultValue.find("(")  == -1
        ):
            return "\""+ prop.defaultValue + "\""
        return prop.defaultValue

    def genDefaultVals(self):
        out = []
        for prop in self.sortedProps:
            if not prop.defaultValue:
                continue
            defaultInit = """,_{name} ({value})""".format(name=self.genRightPaddedName(prop.propDataType().name)
                                                           , value=self.quoteVal(prop))
            out.append(defaultInit)
        return '\n'.join(out)

    @staticmethod
    def generateMsgInclude(msg):
        return "#include <%s/Messages/%s.h>\n" % (Renderer.generateInclDirForNamespace(msg), msg.name)

    @staticmethod
    def generateFieldInclude(field):
        return "#include <%s/Fields/%s.h>\n" % (Renderer.generateInclDirForNamespace(field), field.name)

    def getResolvedPropName(self, prop):
        pass

    def generateIncludes(self):
        out =  Renderer.generateMsgInclude(self.message.baseMessage) if self.message.baseMessage else ""
        for prop in self.message.props:
            field = prop.propDataType()
            if field.objectType() == ObjectType.Message:
                out = out + Renderer.generateMsgInclude(field)
            else:
                out = out + Renderer.generateFieldInclude(field)

        return out

    def generateMembers(self):
        out = ""
        for prop in self.message.props:
            self.genPropType(prop)
            out = out + self.genPropType(prop) + "\n"
        return out

    def applyMemberNamesToString(self, pattern, onlyRequired = False):
        def condition(prop, onlyRequired):
            if onlyRequired == True:
                return prop.required() == True
            return True

        args = tuple([self.genRightPaddedName('_' + prop.name) for prop in self.message.props if condition(prop, onlyRequired)  ])
        return pattern % args

    def genPropType(self, prop):
        prefix = renderers.common.Renderer.genQualifiedNS(prop.propDataType(), self.message.namespace)
        return prefix + '::' +  prop.propDataType().className if len(prefix) > 0 else prop.propDataType().className

    def genBaseClass(self):
        if self.message.baseMessage == None:
            return "Lib::ContainerType";
        prefix = renderers.common.Renderer.genQualifiedNS(self.message.baseMessage, self.message.namespace)
        return prefix + '::' + self.message.baseMessage.name if len(prefix) > 0 else self.message.baseMessage.name
