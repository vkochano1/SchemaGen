import model.common
class Loader(object):
    @staticmethod
    def processMethods(modelObj, element):
        if hasattr(element, 'Method'):
            for method in element.Method:
                name = method["Name"]
                declaration = method["Declaration"]
                modelObj.addMethod(model.common.Method(name, declaration))
