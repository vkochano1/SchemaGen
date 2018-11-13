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
        injects = messageElement["Injects"]

        msgArgs = {
        "name" : messageElement["Name"],
        "namespace" : namespace,
        "tag" : messageElement["Tag"],
        "isAbstract" : str(messageElement["Abstract"]).lower() == "true",
        "isPolymorphic" : str(messageElement["Polymorphic"]).lower() == "true",
        "basename" : messageElement["Extends"],
        "usingNamespace" : messageElement["Using"],
        "alias" : messageElement["Alias"],
        "displayName" : messageElement["DisplayName"]
        }

        message = model.message.Message(**msgArgs);
        if injects != None:
            message.addProperty( model.property.InjectionProperty(injects))

        Loader.processMessageProperties(message, messageElement)

        loader.common.Loader.processMethods(message, messageElement)

        return message
