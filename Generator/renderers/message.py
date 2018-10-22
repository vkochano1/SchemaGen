import model.namespace
import renderers.common
class Renderer:
    def __init__(self, model, message):
        self.model = model
        self.message = message
        self.propMaxLen = 0
        self.hasMessageVectorProp = False
        self.countPropsRequired = 0
        self.countPropsAll = len(self.message.props)
        for prop in self.message.props:
            self.propMaxLen = max(self.propMaxLen, len(self.genPropType(prop)))
            self.hasMessageVectorProp = self.hasMessageVectorProp or (prop.field.objType == "Message" and prop.field.isVector)
            if prop.required == True:
                self.countPropsRequired = self.countPropsRequired + 1
    @staticmethod
    def generateInclDirForNamespace( obj):
        return  '/'.join( obj.namespace.components[1:])

    def genRightPaddedName(self, name):
        return name + ' ' * (self.propMaxLen - len(name))

    def genDefaultVals(self):
        out = []
        for prop in self.message.props:
            if not prop.defaultValue:
                continue
            defaultInit = ",{name} ({value})".format(name=self.genRightPaddedName(prop.field.name), value=prop.defaultValue)
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
            field = prop.field
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
                return prop.required == True
            return True

        args = tuple([self.genRightPaddedName('_' + prop.name) for prop in self.message.props if condition(prop, onlyRequired)  ])
        return pattern % args

    def genPropType(self, prop):
        prefix = renderers.common.Renderer.genQualifiedNS(prop.field, self.message.namespace)
        return prefix + '::' +  prop.field.className if len(prefix) > 0 else prop.field.className

    def genBaseClass(self):
        if self.message.baseMessage == None:
            return "Lib::ContainerType";
        prefix = renderers.common.Renderer.genQualifiedNS(self.message.baseMessage, self.message.namespace)
        return prefix + '::' + self.message.baseMessage.name if len(prefix) > 0 else self.message.baseMessage.name
