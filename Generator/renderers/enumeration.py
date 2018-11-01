import model.namespace

class Renderer:
    def __init__(self, model, enum):
        self.model = model
        self.enum = enum
        self.nameMaxLen = max([len(name) for name, _ in enum.nameValueArr])

    def genRightPaddedName(self, name):
        return name + ' ' * (self.nameMaxLen - len(name))

    def generateEnumValues(self):
        return ',\n'.join([self.genRightPaddedName(name) + ' = ' +  str(value)\
                    for name, value in self.enum.nameValueArr])
