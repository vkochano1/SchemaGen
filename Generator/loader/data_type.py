import os
import importlib
import sys
import utils

@utils.singleton
class Loader(object):
    def __init__(self):
        self.dataTypeName = {}
        path = '/'.join(os.path.realpath(__file__).split('/')[:-1])

        dir = os.path.join(path, "../datatypes")
        sys.path.append(dir)

        for f in os.listdir(dir):
            if not f.endswith('.py') or f.startswith('__'):
                continue
            name = os.path.splitext(f)[0]
            pkg = importlib.import_module(name)
            traits = getattr(pkg, "Traits")
            self.dataTypeName [name] = traits


    def processDataTypeElements(self, element, namespace = None):
        class CustomDataType(object):
            def __init__(self, name, isSimpleType = True):
                self.includes = []
                self.additionalBaseClasses =[]
                self.specialTemplateFile = ""
                self.simpleType = isSimpleType
                self.name = name

        if hasattr(element, 'DataType'):
            for dataType in element.DataType:
                name = dataType["Name"]
                self.dataTypeName[name] = CustomDataType(name)
