import model.namespace

class Renderer:
    def __init__(self, model, enum):
        self.model = model
        self.enum = enum
        self.nameMaxLen = max([len(name) for name, _ in enum.nameValueArr])

    def genRightPaddedName(self, name):
        return name + ' ' * (self.nameMaxLen - len(name))

    def applyEnumNamesToString(self, pattern):
        args = tuple([self.genRightPaddedName(name) for name,  _ in self.enum.nameValueArr])
        return pattern % args

    def applyEnumNameValsToString(self, pattern):
        args = []
        for name,  val in self.enum.nameValueArr:
            args.append(self.genRightPaddedName(name))
            args.append(val)
        return pattern % tuple(args)

    def generateEnumValues(self):

        return ',\n'.join([self.genRightPaddedName(name) + ' = ' +  str(value)\
                    for name, value in self.enum.nameValueArr])
