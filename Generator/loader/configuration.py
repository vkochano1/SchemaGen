import property
import loader.common
import model.configuration

class Loader(object):
    @staticmethod
    def processConfProperties(conf, confElement):
        propLoader = property.Loader()
        for el in  confElement.get_elements():
            if el._name in ['Property', 'Injects', 'Vector']:
                conf.addProperty(propLoader.load(el))

    @staticmethod
    def load(namespace, confElement):
        injects = confElement["Injects"]

        msgArgs = {
        "name" : confElement["Name"],
        "namespace" : namespace,
        "tag" : confElement["Tag"],
        "isAbstract" : str(confElement["Abstract"]).lower() == "true",
        "isPolymorphic" : str(confElement["Polymorphic"]).lower() == "true",
        "basename" : confElement["Extends"],
        "usingNamespace" : confElement["Using"],
        "alias" : confElement["Alias"],
        "displayName" : confElement["DisplayName"]
        }

        conf = model.configuration.Configuration(**msgArgs);
        if injects != None:
            message.addProperty( model.property.InjectionProperty(injects))

        Loader.processConfProperties(conf, confElement)

        loader.common.Loader.processMethods(conf, confElement)

        return conf
