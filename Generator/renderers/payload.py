import renderers.message
import model.namespace
import renderers.common
from  model.common import *

class Renderer(renderers.message.Renderer):
    def __init__(self, model, payload):
        renderers.message.Renderer.__init__(self, model, payload)

    @staticmethod
    def generatePayloadInclude(msg):
        return "#include <%s/Payloads/%s.h>\n" % (Renderer.generateInclDirForNamespace(msg), msg.name)

    def generateIncludes(self):
        out =  Renderer.generatePayloadInclude(self.message.baseMessage) if self.message.baseMessage else ""
        for prop in self.message.props:
            dt = prop.propDataType()
            if dt.objectType() == ObjectType.Message:
                out = out + Renderer.generateMsgInclude(dt)
            elif dt.objectType() == ObjectType.Payload:
                out = out + Renderer.generatePayloadInclude(dt)
            else:
                out = out + Renderer.generateFieldInclude(dt)
        return out

    def genBaseClass(self):
        if self.message.baseMessage == None:
            return "Lib::PayloType";
        prefix = renderers.common.Renderer.genQualifiedNS(self.message.baseMessage, self.message.namespace)
        return prefix + '::' + self.message.baseMessage.name if len(prefix) > 0 else self.message.baseMessage.name
