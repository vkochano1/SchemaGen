import os
import logging

class Environment(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.includePaths = []

    def addIncludePath(self, path):
        if os.path.exists(path):
            self.includePaths.append(path)

    def lookupFile(self, filename):
        self.logger.debug("Searching for file %s" % filename)
        for path in self.includePaths:
            pathToCheck = os.path.join(path, filename)
            self.logger.debug("Checking existence of %s" % pathToCheck)
            if os.path.exists(pathToCheck):
                self.logger.info("Include file %s was resolved as  %s" % (filename, pathToCheck))
                return pathToCheck
        return None
