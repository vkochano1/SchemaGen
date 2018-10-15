import property
import loader.common
import model.message

class Loader(object):
    @staticmethod
    def processMessageProperties(message, messageElement):
        propLoader = property.Loader()
        for el in  messageElement.get_elements():
            if el._name in ['Property', 'Injects', 'Vector']:
                message.addProperty(propLoader.load(el))

    @staticmethod
    def load(namespace, messageElement):
        name = messageElement["Name"]
        tag = messageElement["Tag"]
        isAbstract = messageElement["Abstract"] or False
        basename = messageElement["Extends"]
        injects = messageElement["Injects"]

        message = model.message.Message(name, tag, namespace, basename, isAbstract);
        if injects != None:
            message.addProperty( model.property.InjectionProperty(injects))

        Loader.processMessageProperties(message, messageElement)

        loader.common.Loader.processMethods(message, messageElement)
        loader.common.Loader.processConstructorBody(message, messageElement)

        return message
