import model.namespace

class Renderer:
    def __init__(self, model, namespace):
        self.model = model
        self.namespace = namespace

    def generateNamespaceBegin(self):
        out = ""

        for component in self.namespace.components:
            if component != '':
                out = out + "\nnamespace %s\n{\n" % (component)
        return out

    def generateNamespaceEnd(self):
        out = ""

        for component in self.namespace.components:
            if component != '':
                out = out + "}\n"
        return out
