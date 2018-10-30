import os
import importlib
import sys
import utils
import model.datatype
import model.schema

@utils.singleton
class Loader(object):
    def __init__(self):
        self.libNamespace = model.schema.Schema().createOrGet("Lib")[-1]
        self.defaultDataTypes = {

     model.datatype.DataType (name = "Boolean", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Flag", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Double", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Integer", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Long", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "String", namespace = self.libNamespace, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "LongString", namespace = self.libNamespace, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "ShortString", namespace = self.libNamespace, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "RegularString", namespace = self.libNamespace, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "Price", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "TimeDuration", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "UtcDateTime", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "LocalDateTime", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "FixedBuffer", namespace = self.libNamespace, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "FixedString", namespace = self.libNamespace, isString = False, isSimpleType = True)
    }
        self.defultDataTypesDict = dict( { (dtype.name, dtype) for dtype in self.defaultDataTypes } )


    def lookUp(self, datatypeName):
        resolved = self.defultDataTypesDict.get(datatypeName)
        if not resolved:
             raise Exception("Failed to resolve datatype %s" % datatypeName)
        return resolved

    def load(self, namespace, enumElement):
        name = enumElement["Name"]
        isString = enumElement["IsString"] if enumElement["IsString"] else False
        return model.datatype.DataType(name, namespace, isString = isString)
