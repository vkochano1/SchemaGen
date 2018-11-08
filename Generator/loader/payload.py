import property
import loader.common
import model.payload

class Loader(object):
    @staticmethod
    def processMessageProperties(message, messageElement):
        propLoader = property.Loader()
        for el in  messageElement.get_elements():
            if el._name in ['Property', 'Injects']:
                message.addProperty(propLoader.load(el))

    @staticmethod
    def load(namespace, messageElement):
        injects = messageElement["Injects"]

        msgArgs = {
        "name" : messageElement["Name"],
        "namespace" : namespace,
        "tag" : messageElement["Tag"],
        "isAbstract" : messageElement["Abstract"] or False,
        "isPolymorphic" : messageElement["Polymorphic"] or False,
        "basename" : messageElement["Extends"],
        "isAbstractHeader" : messageElement["isAbstractHeader"] or False
        }

        message = model.message.Payload(**msgArgs);
        if injects != None:
            message.addProperty( model.property.InjectionProperty(injects))

        Loader.processMessageProperties(message, messageElement)

        loader.common.Loader.processMethods(message, messageElement)

        return message
