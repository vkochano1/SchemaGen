import os
import importlib
import sys
import utils
import model.datatype
import model.schema
from model.common import *

class Loader(object):
    @staticmethod
    def load(namespace, dataTypeElement):
        name = dataTypeElement["Name"]
        name = name.replace("[*]","") # attributes can be applied to any datatype
        attrIsString = dataTypeElement["IsString"]
        isString = attrIsString.lower() == "true" if attrIsString else False

        attrHeaderFile = dataTypeElement["HeaderPath"]
        headerFile = attrHeaderFile if attrHeaderFile  else None

        attrIsDerivedFromSimpleType = dataTypeElement["IsDerivedFromSimpleType"]
        isSimpleType = attrIsDerivedFromSimpleType.lower() == "true" if attrIsDerivedFromSimpleType else False

        attrRank = dataTypeElement["TypeRank"]
        rank = int(attrRank) if attrRank else MAX_PROP_RANK

        dataType = model.datatype.DataType(name, namespace
                                      , isSimpleType =  isSimpleType
                                      , isString = isString
                                      , headerFile = headerFile
                                      , rank = rank)

        return dataType
