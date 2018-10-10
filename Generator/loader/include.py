import environment
import untangle

class IncludeFile(object):
    def __init__(self, filename, env, includedFiles):
        self.processIncudeFile(filename, env, includedFiles)

    def processIncludeElements(self, element,  env, processedFiles):
        if hasattr(element, "Include"):
            for inclFile in element.Include:
                name = inclFile['File']
                tmp = IncludeFile(name, env, processedFiles)


    def processIncudeFile(self, filename, env, processedFiles):
        resolvedFile = env.lookupFile(filename)

        processedFilePaths = set([file.resolvedFile for file in processedFiles])
        if resolvedFile in processedFilePaths:
            return None

        self.filename = filename
        self.resolvedFile = resolvedFile
        self.Schema = untangle.parse(resolvedFile).Schema
        processedFiles.add(self)
        self.processIncludeElements(self.Schema, env, processedFiles)

        if hasattr(self.Schema, "Namespace"):
            for namespaceEl in self.Schema.Namespace:
                self.processIncludeElements(namespaceEl, env, processedFiles)
