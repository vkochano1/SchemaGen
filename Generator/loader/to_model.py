import environment
import include
import model.message
import model.field
import model.namespace
import model.schema
import model.property
import model.enumeration
import loader.data_type

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

    def processFieldElements(self, currentEl, namespace):
        if hasattr(currentEl, 'Field'):
            self.namespacesWithFields.append((namespace, currentEl.Field) )

    def processMessageElements(self, currentEl, namespace):
        if hasattr(currentEl, 'Message'):
            self.namespacesWithMessages.append((namespace, currentEl.Message))

    def processEnumerationElements(self, currentEl, namespace):
        if hasattr(currentEl, 'Enumeration'):
            self.namespacesWithEnumerations.append((namespace, currentEl.Enumeration))

    def processImportElements(self, currentEl, namespace):
        if hasattr(currentEl, 'Import'):
                for imp in currentEl.Import:
                    resolvedImportedNamespaceName = imp["Namespace"]
                    namespace.importNamespace(resolvedImportedNamespaceName)

    def processNamespace(self, namespaceEl):
        name = namespaceEl["Name"]
        resolvedNamespace = self.modelNamespaces.createOrGet(name)[-1]

        loader.data_type.Loader().processDataTypeElements(namespaceEl)
        self.processEnumerationElements(namespaceEl, resolvedNamespace)
        self.processFieldElements(namespaceEl, resolvedNamespace)
        self.processMessageElements(namespaceEl, resolvedNamespace)
        self.processImportElements(namespaceEl, resolvedNamespace)

    def prepareDataPass(self):
        for includedFile in self.includedFiles:
            if hasattr(includedFile.Schema, 'Namespace'):
                for namespace in includedFile.Schema.Namespace:
                    self.processNamespace(namespace)

    def validateDataPass(self):
        pass

    def linkDataPass(self):
        for resolvedNamespace, enumElements in self.namespacesWithEnumerations:
            self.processEnumerations(resolvedNamespace, enumElements)

        for resolvedNamespace, fieldElements in self.namespacesWithFields:
            self.processFields(resolvedNamespace, fieldElements)

        for resolvedNamespace, messageElements in self.namespacesWithMessages:
            self.processMessages(resolvedNamespace, messageElements)

    def processIncludedFiles(self):
        self.prepareDataPass()
        self.linkDataPass()
        self.validateDataPass()

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
            isAbstract = messageElement["Abstract"] or False
            basename = messageElement["Extends"]

            message = model.message.Message(name, tag, namespace, basename, isAbstract);
            self.processMessageProperties(namespace, message, messageElement)
            self.processMethods(message, messageElement)
            self.processConstructorBody(message, messageElement)

            namespace.addMessage(message)

    def processMessageProperties(self, namespace, message, messageElement):
        for el in  messageElement.get_elements():
            if el._name == 'Property':
                name = el["Name"]
                required = el["Required"]
                defaultValue = el["Default"]
                message.addProperty( model.property.Property(name, required, defaultValue) )
            elif el._name == 'Injects':
                name = el["Name"]
                message.addProperty( model.property.InjectionProperty(name))
            elif el._name == 'Vector':
                required = el["Required"]
                name = el["Name"]
                message.addProperty( model.property.VectorProperty(name,required))

    def processMethods(self, modelObj, element):
        if hasattr(element, 'Method'):
            for method in element.Method:
                declaration = method["Declaration"]
                modelObj.addMethod(declaration)

    def processConstructorBody(self, modelObj, element):
        if hasattr(element, 'constructor_body'):
            if len(element.constructor_body) > 1:
                raise Exception("Multiple constructor bodies")
            declaration = method["Declaration"][0]
            modelObj.setConstructorBody(declaration)
