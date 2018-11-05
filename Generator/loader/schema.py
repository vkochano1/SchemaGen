import environment
import include
import model.message
import model.field
import model.namespace
import model.schema
import model.property
import model.enumeration
import model.schema
import loader.namespace
import utils
import logging

class Loader(object):
    def __init__(self, filename, env):
        self.logger = logging.getLogger(__name__)

        self.includedFiles = set()
        self.schema =  model.schema.Schema()
        self.namespacesToVisit =  []
        self.rootFile = include.IncludeFile(filename, env, self.includedFiles)

    def traverseNamespace(self, element, parentNamespaceStr  = ''):
        if hasattr(element, 'Namespace'):
            for namespace in element.Namespace:
                currentNamespaceStr = loader.namespace.Loader.preload(self.schema
                                                                    , namespace
                                                                    , parentNamespaceStr)

                self.namespacesToVisit.append((currentNamespaceStr, namespace))
                self.traverseNamespace(namespace, currentNamespaceStr)

    def prepareDataPass(self):
        for includedFile in self.includedFiles:
            self.logger.info('Processing include file %s' % includedFile.filename)
            self.traverseNamespace(includedFile.Schema, '')

    def validateDataPass(self):
        pass

    def linkDataPass(self):
        for fullName, element in self.namespacesToVisit:
            loader.namespace.Loader.load(self.schema, element, fullName)

        self.schema.resolveLinks()

    def load(self):
        self.prepareDataPass()
        self.linkDataPass()
        self.validateDataPass()
        return self.schema
