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
                , skipNamespaces = ''):
        self.REVISION = "1"
        self.projectDir = projectDir
        self.includeDirs = [os.path.join(self.projectDir, name.strip()) for name in includeDirs.split(';')]
        self.outDir = os.path.join(projectDir,outDir)
        self.schemaFile = schemaFile
        self.logName = os.path.join(projectDir,logName)
        self.skipNamespaces = [name.strip() for name in skipNamespaces.split(';')]
        self.env = loader.environment.Environment()

        for includeDir in self.includeDirs:
            self.env.addIncludePath(includeDir)

        format = '%(name)-20s:%(levelname)-8s: %(message)s'
        logging.basicConfig(level=logging.DEBUG, format = format)

    def needToRenderNamespace(self, namespace):
        return not (namespace in self.skipNamespaces)


class Loader(object):
    def __init__(self, projectFilePath):
        self.logger = logging.getLogger(__name__)
        loader.datatype.Loader()
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
            if name  == 'IncludeDir':
                includeDirs = prop.cdata if prop.cdata else ''
            elif name == 'OutDir':
                outDir = prop.cdata
            elif name == 'LogName':
                logName = prop["name"]
            elif name == 'SchemaFile':
                schemaFile = prop.cdata
            elif name == 'SkipNamespaces':
                skipNamespaces = prop.cdata if prop.cdata else ''

        cfg = Config(self.baseDir, includeDirs, outDir, schemaFile, logName, skipNamespaces)
        schemaLoader = loader.schema.Loader(schemaFile, cfg.env)
        self.schemas.append((schemaLoader, cfg))

    def load(self):
        if hasattr(self.projectFile, 'codeSmith'):
            for project in self.projectFile.codeSmith:
                if hasattr(project, 'PropertySets'):
                    for propSets in project.PropertySets:
                        if hasattr(propSets, 'PropertySet'):
                                for propSet in propSets.PropertySet:
                                    self.loadPropSet(propSet)
