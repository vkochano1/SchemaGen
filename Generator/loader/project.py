import loader.schema
import loader.environment
import loader.datatype
import logging
import untangle

class Config(object):
    def __init__(self, includeDirs, outDir, schemaFile, logName, skipNamespaces = ''):
        self.REVISION = "12345"
        self.includeDirs = [name.strip() for name in includeDirs.split(';')]
        self.outDir = outDir
        self.schemaFile = schemaFile
        self.logName = logName
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
        self.projectFile = untangle.parse(projectFilePath)
        self.schemas = []

    def loadPropSet(self, propSet):
        includeDirs = ''
        schemaFile = None
        outDir = None
        logName = None
        skipNamespaces = ''

        for prop in propSet.get_elements():
            if prop._name   == 'IncludeDir':
                includeDirs = prop["name"] if prop["name"] else ''
            elif prop._name == 'OutDir':
                outDir = prop["name"]
            elif prop._name == 'LogName':
                logName = prop["name"]
            elif prop._name == 'SchemaFile':
                schemaFile = prop["name"]
            elif prop._name == 'SkipNamespaces':
                skipNamespaces = prop["name"] if prop["name"] else ''

        cfg = Config(includeDirs, outDir, schemaFile, logName, skipNamespaces)
        schemaLoader = loader.schema.Loader(schemaFile, cfg.env)
        self.schemas.append((schemaLoader, cfg))

    def load(self):
        if hasattr(self.projectFile, 'codeSmith'):
            for project in self.projectFile.codeSmith:
                if hasattr(project, 'PropertySets'):
                    for propSets in project.PropertySets:
                        if hasattr(propSets, 'PropertySet'):
                                for prop in propSets.PropertySet:
                                    self.loadPropSet(prop)
