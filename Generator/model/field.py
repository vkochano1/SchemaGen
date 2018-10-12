import namespace
import loader.data_type
import logging

class Field(object):
    def __init__(self, fullName, tag, datatype, myNamespace):
        self.logger = logging.getLogger(__name__)
        self.tag = tag
        self.dataTypeName = datatype
        self.dataType = None
        self.namespace = myNamespace
        self.name = fullName
        self.logger.debug('Created field %s::%s ' % (myNamespace.fullName, self.name))

    def __str__(self):
        return "\n{\n field:'%s::%s',\n tag:'%s',\n data_type:%s\n}\n" % (
        self.namespace.fullName,
        self.name,
        str(self.tag),
        str(self.dataType)
        )

    def __repr__(self):
        return str(self.__dict__)

    def resolveLinks(self):
        self.dataType = self.namespace.resolveEnumByName(self.dataTypeName)
        if self.dataType == None:
            self.dataType = loader.data_type.Loader().dataTypeName[self.dataTypeName]
