import model.message
import property
import logging
import utils
from common import *

class Payload(model.message.Message):
    def __init__(self, name, tag, namespace
                , basename = None
                , isAbstract = False
                , isPolymorphic = False
                , usingNamespace = None
                , alias = None
                , displayName = None
                , isAbstractHeader = True
                , payloadSize = 0):
        super(Payload, self).__init__(name, tag, namespace, basename = basename)
        self.isAbstractHeader = isAbstractHeader
        self.changeObjectType(ObjectType.Payload)
        self.attributes = []
        self.payloadSize = payloadSize
        self.isAbstractHeader = isAbstractHeader

    def addAttribute(self, attr):
        self.attributes.append(attr)

    def resolveBase(self):
        if None == self.basename:
            return None
        resolvedMsg = self.namespace().resolvePayloadByName(self.basename)
        if resolvedMsg == None:
            raise Exception('Failed to resolve base class %s' % self.basename)
        return resolvedMsg
