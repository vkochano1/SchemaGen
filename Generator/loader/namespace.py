import property
import loader.common
import model.namespace
import loader.data_type
import loader.message
import loader.field
import loader.enumeration
import utils

class Loader(object):
    @staticmethod
    def preload(modelNamespaces, namespaceEl, parentNamespaceStr):
        fullName = utils.NamespacePath.concatNamespaces(parentNamespaceStr, namespaceEl["Name"])
        ns = modelNamespaces.createOrGet(fullName)[-1]
        Loader.processImportElements(namespaceEl, ns)
        return fullName

    @staticmethod
    def load(modelNamespaces, namespaceEl, fullName):
        resolvedNamespace = modelNamespaces.createOrGet(fullName)[-1]

        loader.data_type.Loader().processDataTypeElements(namespaceEl)
        Loader.processEnumerations(namespaceEl, resolvedNamespace)
        Loader.processFields(namespaceEl, resolvedNamespace)
        Loader.processMessages(namespaceEl, resolvedNamespace)
        return resolvedNamespace

    @staticmethod
    def processImportElements(currentEl, namespace):
        if hasattr(currentEl, 'Import'):
            for imp in currentEl.Import:
                resolvedImportedNamespaceName = imp["Namespace"]
                namespace.importNamespace(resolvedImportedNamespaceName)

    @staticmethod
    def processFields(currentEl, namespace):
        if hasattr(currentEl, 'Field'):
            for fieldElement in currentEl.Field:
                namespace.addField(loader.field.Loader.load(namespace, fieldElement))

    @staticmethod
    def processEnumerations(currentEl, namespace):
        if hasattr(currentEl, 'Enumeration'):
            for enumElement in currentEl.Enumeration:
                namespace.addEnum(loader.enumeration.Loader.load(namespace, enumElement))

    @staticmethod
    def processMessages(currentEl, namespace):
        if hasattr(currentEl, 'Message'):
            for messageElement in currentEl.Message:
                namespace.addMessage(loader.message.Loader.load(namespace, messageElement))