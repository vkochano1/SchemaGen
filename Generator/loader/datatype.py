import os
import importlib
import sys
import utils
import model.datatype

@utils.singleton
class Loader(object):
    def __init__(self):
        self.defaultDataTypes = {

     model.datatype.DataType (name = "Boolean", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Flag", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Double", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Integer", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "Long", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "String", namespace = None, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "LongString", namespace = None, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "ShortString", namespace = None, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "RegularString", namespace = None, isString = True, isSimpleType = True)
    ,model.datatype.DataType (name = "Price", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "TimeDuration", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "UtcDateTime", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "LocalDateTime", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "FixedBuffer", namespace = None, isString = False, isSimpleType = True)
    ,model.datatype.DataType (name = "FixedString", namespace = None, isString = False, isSimpleType = True)
    }
        self.defultDataTypesDict = dict( { (dtype.name, dtype) for dtype in self.defaultDataTypes } )


    def lookUp(self, datatypeName):
        resolved = self.defultDataTypesDict.get(datatypeName)
        if not resolved:
             raise Exception("Failed to resolve datatype %s" % datatypeName)
        return resolved

    def load(self, namespace, enumElement):
        name = enumElement["Name"]
        return model.datatype.DataType(name, namespace)
