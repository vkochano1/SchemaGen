import loader.schema
import loader.environment
import loader.datatype
import logging
import untangle
import os

class Config(object):
    def __init__( self, projectDir
                , includeDirs, outDir
                , schemaFile, logName
                , skipNamespaces = None):
        self.REVISION = "1"
        self.projectDir = projectDir
        includeDirs = includeDirs.replace(",",";")
        self.includeDirs = [os.path.join(self.projectDir, name.strip()) for name in includeDirs.split(';')]
        self.includeDirs.append(projectDir)
        self.outDir = os.path.join(projectDir,outDir)
        self.schemaFile = schemaFile
        self.logName = os.path.join(projectDir,logName)
        self.skipNamespaces = []
        if skipNamespaces:
            self.skipNamespaces = [name.strip() for name in skipNamespaces.split(';')]
        self.env = loader.environment.Environment()

        for includeDir in self.includeDirs:
            self.env.addIncludePath(includeDir)

        format = '%(name)-20s:%(levelname)-8s: %(message)s'
        logging.basicConfig(level=logging.INFO, format = format)

    def needToRenderNamespace(self, namespace):
        for toSkip in self.skipNamespaces:
            if namespace.find(toSkip) == 0:
                return False
        return True


class Loader(object):
    def __init__(self, projectFilePath):
        self.logger = logging.getLogger(__name__)
        projDir, filename = os.path.split(projectFilePath)
        self.baseDir = os.path.abspath(projDir)
        self.projectFile = untangle.parse(projectFilePath)
        self.schemas = []

    def loadPropSet(self, propSet):
        includeDirs = ''
        schemaFile = None
        outDir = None
        logName = 'tmp.log'
        skipNamespaces = ''

        for prop in propSet.property:
            name = prop["name"]
            if name  == 'IncludePath':
                includeDirs = prop.cdata if prop.cdata else ''
            elif name == 'OutputDir':
                outDir = prop.cdata
            elif name == 'LogName':
                logName = prop["name"]
            elif name == 'Schema':
                schemaFile = prop.cdata
            elif name == 'SkipNamespaces':
                skipNamespaces = prop.cdata if prop.cdata else ''

        cfg = Config(self.baseDir, includeDirs, outDir, schemaFile, logName, skipNamespaces)
        loader.datatype.Loader()
        schemaLoader = loader.schema.Loader(schemaFile, cfg.env)
        self.schemas.append((schemaLoader, cfg))

    def load(self):
        if hasattr(self.projectFile, 'codeSmith'):
            for project in self.projectFile.codeSmith:
                if hasattr(project, 'propertySets'):
                    for propSets in project.propertySets:
                        if hasattr(propSets, 'propertySet'):
                                for propSet in propSets.propertySet:
                                    self.loadPropSet(propSet)
