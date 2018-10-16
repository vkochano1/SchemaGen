import environment
import include
import model.message
import model.field
import model.namespace
import model.schema
import model.property
import model.enumeration
import loader.namespace
import logging

class ModelLoader(object):
    def __init__(self, filename, env):
        self.logger = logging.getLogger(__name__)

        self.includedFiles = set()
        self.modelNamespaces =  model.namespace.Namespaces()
        self.rootFile = include.IncludeFile(filename, env, self.includedFiles)
        self.processIncludedFiles()

    def prepareDataPass(self):
        for includedFile in self.includedFiles:
            self.logger.info('Processing include file %s' % includedFile.filename)
            if hasattr(includedFile.Schema, 'Namespace'):
                for namespace in includedFile.Schema.Namespace:
                    loader.namespace.Loader.preload(self.modelNamespaces, namespace)

    def validateDataPass(self):
        pass

    def linkDataPass(self):
        for includedFile in self.includedFiles:
            if hasattr(includedFile.Schema, 'Namespace'):
                for namespace in includedFile.Schema.Namespace:
                    loader.namespace.Loader.load(self.modelNamespaces, namespace)


        self.modelNamespaces.resolveLinks()

    def processIncludedFiles(self):
        self.prepareDataPass()
        self.linkDataPass()
        self.validateDataPass()
