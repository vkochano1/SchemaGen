import namespace
import logging
import utils
import copy
from common import *

class Field(ModelObject):
    def __init__(self, name, tag, dataType, namespace, attrs = None, displayName = None):
        super(Field, self).__init__(ObjectType.Field, namespace, name)
        self.className = 'Field' + self.name
        self.displayName = displayName
        self.tag = tag
        self.dataTypeName = dataType
        self.dataType = None
        self.attrs = attrs
        self.logger.debug('Created field %s::%s ' % (namespace.fullName, self.name))

    def __str__(self):
        return "{{ Field:'{name}',Tag:'{tag}', Datatype: '{datatype}' }}".format(name=self.fullName, tag = self.tag, datatype = str(self.dataType))

    def __repr__(self): return str(self)

    def resolveLinks(self):
        self.dataType = self.namespace().resolveDataTypeByName(self.dataTypeName)
        if self.dataType == None:
            self.dataType = self.namespace().resolveDataTypeByName("Lib::" + self.dataTypeName)

        if self.dataType == None:
            raise Exception('Failed to resolve datatype %s' % str(self.dataTypeName))

        if self.attrs != None:
            ## need to create new data type with field atributes
            cloned = copy.copy(self.dataType)
            self.dataType.fullName = cloned.namespace().fullName + "::" + cloned.name + "<" + ','.join(self.attrs) + ">"
            self.dataType = cloned
        self.changePropDataCategory(self.dataType.propDataCategory())
