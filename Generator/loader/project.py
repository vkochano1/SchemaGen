import loader.schema
import loader.environment
import loader.data_type
import logging
import untangle

class Config(object):
    def __init__(self, includeDirs, outDir, schemaFile, logName):
        self.REVISION = "12345"

        self.includeDirs = [name.strip() for name in includeDirs.split(';')]
        self.outDir = outDir
        self.schemaFile = schemaFile
        self.logName = logName

        self.env = loader.environment.Environment()

        for includeDir in self.includeDirs:
            self.env.addIncludePath(includeDir)

        format = '%(name)-20s:%(levelname)-8s: %(message)s'
        logging.basicConfig(level=logging.DEBUG, format = format)

    def needToRenderNamespace(self, namespace):
        return not namespace.fullName.startswith("Z::F")


class Loader(object):
    def __init__(self, projectFilePath):
        self.logger = logging.getLogger(__name__)
        types = loader.data_type.Loader()
        self.projectFile = untangle.parse(projectFilePath)
        self.schemas = []

    def loadPropSet(self, propSet):
        includeDirs = None
        schemaFile = None
        outDir = None
        logName = None

        for prop in propSet.get_elements():
            if prop._name   == 'IncludeDir':
                includeDirs = prop["value"]
            elif prop._name == 'OutDir':
                outDir = prop["value"]
            elif prop._name == 'LogName':
                logName = prop["value"]
            elif prop._name == 'SchemaFile':
                schemaFile = prop["value"]

        cfg = Config(includeDirs, outDir, schemaFile, logName)
        schemaLoader = loader.schema.Loader(schemaFile, cfg.env)
        self.schemas.append((schemaLoader, cfg))

    def load(self):
        if hasattr(self.projectFile, 'Project'):
            for project in self.projectFile.Project:
                if hasattr(project, 'PropertySets'):
                    for propSets in project.PropertySets:
                        if hasattr(propSets, 'PropertySet'):
                                self.loadPropSet(propSets.PropertySet)
