import property
import loader.common
import model.payload

class Loader(object):
    @staticmethod
    def processPayloadProperties(payload, messageElement):
        propLoader = property.Loader()
        for el in  messageElement.get_elements():
            if el._name == 'Attribute':
                attr = model.property.Attribute(el["Name"], el["ConstantValue"])
                payload.addAttribute(attr)
            elif el._name == 'Property':
                payload.addProperty(propLoader.load(el))

    @staticmethod
    def load(namespace, payloadElement):

        msgArgs = {
        "name" : payloadElement["Name"],
        "namespace" : namespace,
        "tag" : payloadElement["Tag"],
        "basename" : payloadElement["Extends"],
        "isAbstractHeader" : payloadElement["AbstractHeader"].lower() == "true" if payloadElement["AbstractHeader"] else False,
        "payloadSize" : int(payloadElement["Size"])
        }

        payload = model.payload.Payload(**msgArgs);

        Loader.processPayloadProperties(payload, payloadElement)

        loader.common.Loader.processMethods(payload, payloadElement)

        return payload
