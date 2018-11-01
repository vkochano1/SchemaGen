import model.property

class Loader(object):
    def __init__(self):
        pass

    def load(self, el):
        if el._name == 'Property':
            name = el["Name"]

            attrRequired = el["Required"]
            required = (attrRequired.lower() == "true") if attrRequired else false

            defaultValue = el["Default"]
            return  model.property.Property(name, required, defaultValue)
        elif el._name == 'Injects':
            name = el["Name"]
            return model.property.InjectionProperty(name)
        elif el._name == 'Vector':
            required = (attrRequired.lower() == "true") if attrRequired else false
            name = el["DataType"]
            return model.property.VectorProperty(name,required)

        raise 'Invalid property element was provided'
