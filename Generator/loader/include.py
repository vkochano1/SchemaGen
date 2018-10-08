import environment
import untangle

class IncludeFile(object):
    def __init__(self, filename, env, includedFiles):
        self.processIncudeFile(filename, env, includedFiles)

    def processIncudeFile(self, filename, env, processedFiles):
        resolvedFile = env.lookupFile(filename)

        processedFilePaths = set([file.resolvedFile for file in processedFiles])
        if resolvedFile in processedFilePaths:
            return None

        self.filename = filename
        self.resolvedFile = resolvedFile
        self.Schema = untangle.parse(resolvedFile).Schema
        processedFiles.add(self)

        if hasattr(self.Schema, "Include"):
            for inclFile in self.Schema.Include:
                name = inclFile['Name']
                tmp = IncludeFile(name, env, processedFiles)
