class Renderer(object):
    def __init__(self, model, config):
        self.model = model
        self.config = config

    def generateRevision(self):
        return "enum {{ SCHEMA_REVISION = {REVISION} }};".format(REVISION = self.config.REVISION)

    def genCharList(self, name):
        return ','.join(["'" + c + "'" for c in name])

    """@staticmethod
    def genQualifiedNS(obj, namespace):
        i = 0
        if obj.namespace == None:
            return ''

        out = ""
        objCompLen = len(obj.namespace.components)
        for comp in namespace.components:
            if i >= objCompLen:
                break
            if obj.namespace.components[i] != comp:
                break
            i = i+1

        ns = '::'.join(obj.namespace.components[i:])
        return ns
    """
    @staticmethod
    def genQualifiedNS(obj, namespace):
        i = 0
        if obj.namespace == None:
            return ''

        return namespace.fullName
