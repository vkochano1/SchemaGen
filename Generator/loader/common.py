class Loader(object):
    @staticmethod
    def processMethods(modelObj, element):
        if hasattr(element, 'Method'):
            for method in element.Method:
                name = method["Name"]
                declaration = method["Declaration"]
                modelObj.addMethod((name, declaration))

    @staticmethod
    def processConstructorBody(modelObj, element):
        if hasattr(element, 'constructor_body'):
            if len(element.constructor_body) > 1:
                raise Exception("Multiple constructor bodies")
            declaration = method["Declaration"][0]
            modelObj.setConstructorBody(declaration)
