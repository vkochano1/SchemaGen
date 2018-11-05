class Renderer(object):
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def generateRevision(self):
        return "enum {{ SCHEMA_REVISION = {REVISION} }};".format(REVISION = self.config.REVISION)

    def genCharList(self, name):
        return ','.join(["'" + c + "'" for c in name])

    @staticmethod
    def genQualifiedNS(obj, namespace):
        if obj.namespace() == None:
            return ''

        return obj.namespace().fullName


    @staticmethod
    def genIncludes(objCategory, collection):
        out = []
        for obj in collection:
            nsPart = '/'.join(obj.namespace().components[1:])
            inclFile = "#include <{nsPart}/{category}/{name}.h>".format(nsPart = nsPart, category = objCategory, name = obj.name)
            out.append(inclFile)

        return '\n'.join(out)
