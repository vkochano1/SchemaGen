import property
import loader.common
import model.payload

class Loader(object):
    @staticmethod
    def processPayloadProperties(payload, messageElement):
        propLoader = property.Loader()
        for el in  messageElement.get_elements():
            if el._name == 'Attribute':
                attr = model.property.Attribute(el["Name"], el["ConstValue"])
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
        "isAbstractHeader" : payloadElement["IsAbstractHeader"].lower() == "true" if payloadElement["IsAbstractHeader"] else False,
        "payloadSize" : int(payloadElement["PayloadSize"])
        }

        payload = model.payload.Payload(**msgArgs);

        Loader.processPayloadProperties(payload, payloadElement)

        loader.common.Loader.processMethods(payload, payloadElement)

        return payload
