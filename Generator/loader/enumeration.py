import property
import loader.common
import model.enumeration

class Loader(object):
    @staticmethod
    def load(namespace, enumElement):
        name = enumElement["Name"]
        items = []
        for item in enumElement.Item:
            itemName = item["Name"]
            itemValue = item["Value"]
            items.append( (itemName, itemValue) )

        newEnum = model.enumeration.Enumeration(name, namespace, items)
        loader.common.Loader.processMethods(newEnum, enumElement)
        return newEnum
