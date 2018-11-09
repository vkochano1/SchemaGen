import model.property

class Loader(object):
    def __init__(self):
        pass

    def load(self, el):
        if el._name == 'Property':
            name = el["Name"]
            attrRequired = el["Required"]
            required = (attrRequired.lower() == "true") if attrRequired else False
            defaultValue = el["DefaultValue"]
            return  model.property.Property(name, required, defaultValue)
        elif el._name == 'Injects':
            name = el["Name"]
            return model.property.InjectionProperty(name)
        elif el._name == 'Vector':
            name = el["DataType"]
            return model.property.VectorProperty(name)

        raise 'Invalid property element'
