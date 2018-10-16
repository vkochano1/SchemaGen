class Renderer(object):
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def generateRevision(self):
        return "enum {{ SCHEMA_REVISION = {REVISION} }}".format(REVISION = self.config.REVISION)

    def genCharList(self, name):
        return ','.join(["'" + c + "'" for c in name])
