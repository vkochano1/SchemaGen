import property
import loader.common
import model.field

class Loader(object):
    @staticmethod
    def load(namespace, fieldElement):
        name = fieldElement["Name"]
        tag = fieldElement["Tag"]
        dataType = fieldElement["DataType"]
        return model.field.Field(name, tag, dataType, namespace)
