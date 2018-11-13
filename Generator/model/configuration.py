import model.message
import property
import logging
import utils
from common import *

class Configuration(model.message.Message):
    def __init__(self, name, tag, namespace
                , basename = None
                , isAbstract = False
                , isPolymorphic = False
                , usingNamespace = None
                , alias = None
                , displayName = None
                , isAbstractHeader = True):
        super(Configuration, self).__init__(name, tag, namespace)
        self._ModelObject__objectType = ObjectType.Configuration

    def resolveBase(self):
        if None == self.basename:
            return None
        resolvedMsg = self.namespace().resolveConfigurationByName(self.basename)

        if not resolvedMsg:
            resolvedMsg = self.namespace().resolveMessageByName(self.basename)
        if resolvedMsg == None:
            raise Exception('Failed to resolve base class %s' % self.basename)
        return resolvedMsg
