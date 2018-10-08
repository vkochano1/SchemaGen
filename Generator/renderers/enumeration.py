import model.namespace

class Renderer:
    def __init__(self, model, enum):
        self.model = model
        self.enum = enum

    def generateEnumValues(self):
        out = ",\n".join([str(name) + '=' + str(value) for name, value in self.enum.nameValueDict.iteritems()])
        return out
