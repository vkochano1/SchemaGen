import os
import importlib
import sys
import utils
import model.namespace
from model.common import *

class Loader(object):
    @staticmethod
    def load(namespace, schemaOffsetEl):
        name = schemaOffsetEl["Enumeration"]
        enumItem = schemaOffsetEl["Value"]
        return model.namespace.SchemaOffset(namespace, name, enumItem)
