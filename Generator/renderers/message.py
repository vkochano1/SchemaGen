import model.namespace

class Renderer:
    def __init__(self, model, message):
        self.model = model
        self.message = message

    def generateIncludes(self):
        out = ""

        for prop in self.message.props:
            field = prop.field
            s1 = '/'.join( field.namespace.components[1:])
            s1 = s1 + '/' + field.name + ".h"

            out = out + "#include<%s>\n" % s1
        return out

    def generateMembers(self):
        out = ""

        for prop in self.message.props:
            field = prop.field
            s1 = '::'.join(field.namespace.components) + '::'
            s1 = s1 + 'Field' + field.name

            out = out + '%s' % s1
        return out
