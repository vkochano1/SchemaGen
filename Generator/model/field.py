import namespace
import loader.datatype
import logging
import utils

class Field(object):
    def __init__(self, fullName, tag, datatype, myNamespace, attrs):
        self.logger = logging.getLogger(__name__)
        self.tag = tag
        self.dataTypeName = datatype
        self.dataType = None
        self.attrs = attrs
        self.namespace = myNamespace
        self.name = fullName
        self.fullName = utils.NamespacePath.concatNamespaces(self.namespace.fullName, self.name)
        self.logger.debug('Created field %s::%s ' % (myNamespace.fullName, self.name))

    def __str__(self):
        return "\n{\n field:'%s::%s',\n tag:'%s',\n datatype:%s\n}\n" % (
        self.namespace.fullName,
        self.name,
        str(self.tag),
        str(self.dataType)
        )

    def __repr__(self):
        return str(self.__dict__)

    def resolveLinks(self):
        self.dataType = self.namespace.resolveDataTypeByName(self.dataTypeName)
        if self.dataType == None:
            self.dataType = loader.datatype.Loader().lookUp(self.dataTypeName)

        if self.dataType == None:
            raise Exception('Failed to resolve datatype %s' % str(self.dataTypeName))
