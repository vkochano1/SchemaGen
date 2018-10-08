import environment
import include
import model.message
import model.field
import model.namespace
import model.schema
import model.property
import model.enumeration

class ModelLoader(object):
    def __init__(self, filename, env):
        self.includedFiles = set()
        self.modelNamespaces =  model.namespace.Namespaces()
        self.rootFile = include.IncludeFile(filename, env, self.includedFiles)
        self.namespacesWithFields =   []
        self.namespacesWithMessages = []
        self.namespacesWithEnumerations = []
        self.importedNamespaces =  []
        self.processIncludedFiles()
        self.modelNamespaces.resolveLinks()

    def processNamespace(self, namespaceEl):
        name = namespaceEl["Name"]
        resolvedNamespace = self.modelNamespaces.createOrGet(name)[-1]

        if hasattr(namespaceEl, 'Field'):
            self.namespacesWithFields.append((resolvedNamespace, namespaceEl.Field) )

        if hasattr(namespaceEl, 'Message'):
            self.namespacesWithMessages.append((resolvedNamespace, namespaceEl.Message))

        if hasattr(namespaceEl, 'Enumeration'):
            self.namespacesWithEnumerations.append((resolvedNamespace, namespaceEl.Enumeration))

        if hasattr(namespaceEl, 'Import'):
                for imp in namespaceEl.Import:
                    resolvedImportedNamespaceName = imp["Namespace"]
                    resolvedNamespace.importNamespace(resolvedImportedNamespaceName)


    def processIncludedFiles(self):
        for includedFile in self.includedFiles:
            if hasattr(includedFile.Schema, 'Namespace'):
                for namespace in includedFile.Schema.Namespace:
                    self.processNamespace(namespace)

        for resolvedNamespace, fieldElements in self.namespacesWithFields:
            self.processFields(resolvedNamespace, fieldElements)

        for resolvedNamespace, messageElements in self.namespacesWithMessages:
            self.processMessages(resolvedNamespace, messageElements)

        for resolvedNamespace, enumElements in self.namespacesWithEnumerations:
            self.processEnumerations(resolvedNamespace, enumElements)

    def processFields(self, namespace, fieldElements):
        for fieldElement in fieldElements:
            name = fieldElement["Name"]
            tag = fieldElement["Tag"]
            dataType = fieldElement["DataType"]

            namespace.addField(model.field.Field(name, tag, dataType, namespace))

    def processEnumerations(self, namespace, enumElements):
        for enumElement in enumElements:
            name = enumElement["Name"]
            items = {}
            for item in enumElement.Item:
                itemName = item["Name"]
                itemValue = item["Value"]
                items[itemName] = itemValue

            namespace.addEnum(model.enumeration.Enumeration(name, namespace, items))

    def processMessages(self, namespace, messageElements):
        for messageElement in messageElements:
            name = messageElement["Name"]
            tag = messageElement["Tag"]
            isAbstract = messageElement["IsAbstract"] or False
            basename = messageElement["Extends"]

            message = model.message.Message(name, tag, namespace, basename, isAbstract);
            self.processMessageProperties(namespace, message, messageElement)
            namespace.addMessage(message)

    def processMessageProperties(self, namespace, message, messageElement):
        if hasattr(messageElement, 'Property'):
            for property in messageElement.Property:
                name = property["Name"]
                required = property["Required"] 
                defaultValue = property["Default"]
                message.addProperty( name, required)
