import os

class Environment(object):
    def __init__(self):
        self.includePaths = []

    def addIncludePath(self, path):
        if os.path.exists(path):
            self.includePaths.append(path)

    def lookupFile(self, filename):
        for path in self.includePaths:
            pathToCheck = os.path.join(path, filename)
            if os.path.exists(pathToCheck):
                print 'resolved ' + str(pathToCheck)
                return pathToCheck
        return None
