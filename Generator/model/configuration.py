import model.message
import model.datatype
import property
import logging
import utils
from common import *


class AtomicStringDataType(ModelObject):

    def __init__(self):
        super(AtomicStringDataType, self).__init__(ObjectType.DataType, None, "Lib::AtomicString")
        self.isSimpleType = False
        self.enumeration = None
        self.headerFile = "Lib/AtomicString.h"
        self.rank = 5
        self.className = "Lib::AtomicString"

    def dataType(self):
        return None

    def propDataCategory(self):
        return PropDataCategory.String

    def namespace(self):
        class dummyNS(object):
            def __init__(self):
                self.fullName = ""
                self.name = ""
                self.components = []
        return dummyNS()

class Configuration(model.message.Message):
    def __init__(self, name, tag, namespace
                , basename = None
                , isAbstract = False
                , isPolymorphic = False
                , usingNamespace = None
                , alias = None
                , displayName = None
                , isAbstractHeader = True):
        super(Configuration, self).__init__(name, tag, namespace, basename = basename)
        self._ModelObject__objectType = ObjectType.Configuration

    def resolveBase(self):
        if None == self.basename:
            return None
        resolvedMsg = self.namespace().resolveConfigurationByName(self.basename)

        if resolvedMsg == None:
            raise Exception('Failed to resolve base class %s' % self.basename)
        return resolvedMsg
