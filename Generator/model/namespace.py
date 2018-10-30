import utils
import logging
import model.datatype
from common import *

class Namespace(ModelObject):
    def __init__(self, name, parentNamespace = None):
        super(Namespace, self).__init__(ObjectType.Namespace, parentNamespace, name)
        # name & topology
        #self.name = name
        self.parentNamespace = parentNamespace
        self.components = self.resolvefullPath_()
        self.subNamespaces = {}
        self.fullName = utils.NamespacePath.componentsToPath(self.components)
        self.isSimpleType = True
        # enumeration data types
        self.enumerations = {}

        # all dataTypes including enumerations
        self.dataTypes  = {}

        self.fieldByName  = {}
        self.messagesByName = {}
        self.fieldByTag   = {}
        self.messagesByTag = {}

        #imported namesapces
        self.importedNamespaces = {}
        self.importedNamespaceNames = set()
        self.importParentNamespaces_()

        self.logger.debug('Created namespace %s' % (self.fullName))

    def __str__(self):
        strCurNamespace  = '\n[\n' + ",\n ".join( str(msg) for name, msg in self.messagesByName.iteritems() ) + '\n]\n'
        strSubNamespaces = '\n[\n' + ', '.join(str(namespace) for namespace in self.subNamespaces.iteritems()) +'\n]\n'
        return  "\n{\n namespace:'%s',\n messages:%s,\n namespaces:%s\n}\n" % (self.fullName, strCurNamespace, strSubNamespaces)

    def __repr__(self):
        return str(self)

    def hasElements(self):
        return 0 < len(self.enumerations) + len(self.messagesByName) + len(self.fieldByName)

    def addField(self, field):
        """Add field to namespace"""
        self.fieldByTag[field.tag] = field
        self.fieldByName[field.name] = field

    def addMessage(self, message):
        """Add message to namespace"""
        self.messagesByTag[message.tag] = message
        self.messagesByName[message.name] = message

    def addEnum(self, enumeration):
        """Add enumeration to namespace"""
        self.enumerations[enumeration.name] = enumeration
        enumDataType = model.datatype.DataType(enumeration.name,enumeration.namespace, enumeration = enumeration)
        self.addDataType(enumDataType)

    def addDataType(self, dataType):
        """Add datatype to namespace"""
        self.dataTypes[dataType.name] = dataType

    def addSubNamespace(self, namespaceName):
        """Create all sub-namesapces for provided path"""
        resolved =  self.subNamespaces.get(namespaceName)
        if resolved:
            return resolved
        resolved = Namespace(namespaceName, self)
        self.subNamespaces[namespaceName] = resolved
        return resolved

    def importNamespace(self, namespaceName):
        """Add namespace name to imported namespaces.
           Actual object resolution is done in resolve links
        """
        self.logger.debug('Importing namespace %s for %s' % (namespaceName, self.fullName))
        self.importedNamespaceNames.add(namespaceName)

    def resolveSubNamesapace(self, prefixPath):
        """Get or create leaf namespace for provided path"""
        currentNamespace = self
        for comp in prefixPath:
            currentNamespace = currentNamespace.subNamespaces.get(comp)
            if currentNamespace == None:
                break
        return currentNamespace

    def resolveByName_(self, nameToResolve, prefixPath, collectionName,  alreadyScanned):
        """Generic  lookup for provided element"""
        if self.fullName in alreadyScanned:
            return None

        namespaceForLookup = self
        if len(prefixPath):
            namespaceForLookup = self.resolveSubNamesapace(prefixPath)
        resolved  = None

        if namespaceForLookup != None:
            collection = getattr(namespaceForLookup, collectionName)
            resolved = collection.get(nameToResolve)

        alreadyScanned.add(self.fullName)

        if None == resolved:
            for name, namespace in self.importedNamespaces.iteritems():
                resolved = namespace.resolveByName_(nameToResolve, prefixPath, collectionName, alreadyScanned)
                if resolved:
                    break

        return resolved

    def resolveDataTypeByName(self, name):
        """Enum element lookup for provided enum name"""
        (prefix, leafName) = utils.NamespacePath.splitFullName(name)
        self.logger.debug('Resolving enum %s'  % (str(name)))
        resolved = self.resolveByName_(leafName, prefix, "dataTypes", set())
        return resolved

    def resolveMessageByName(self, name):
        """Message element lookup for provided message name"""
        self.logger.debug('Resolving message %s'  % (str(name)))
        (prefix, leafName) = utils.NamespacePath.splitFullName(name)
        resolved = self.resolveByName_(leafName, prefix, "messagesByName", set())
        return resolved

    def resolveFieldByName(self, name):
        """Field element lookup for provided field name"""
        self.logger.debug('Resolving field %s'  % (str(name)))
        (prefix, leafName) = utils.NamespacePath.splitFullName(name)
        resolved =  self.resolveByName_(leafName, prefix, "fieldByName", set())
        return resolved

    def resolveImports(self, namespaces):
        for name in self.importedNamespaceNames:
            self.logger.debug('Trying to import namespace %s' % (name))
            #resolved = namespaces.get(name)
            resolved = None

            for _, parentNamespace in  self.importedNamespaces.iteritems():
                lookupName = utils.NamespacePath.concatNamespaces(parentNamespace.fullName, name)
                resolved = namespaces.get(lookupName)
                if resolved != None:
                    break

            if resolved == None:
                self.logger.error('Failed to import namespace %s trying to proceeed anyway' % (name))
                continue

            self.importedNamespaces[name] = resolved

    def resolveLinks(self, namespaces):
        """Once all schema elements added to the model
          object links can be populated """

        for name, message in self.messagesByName.iteritems():
            message.resolveLinks()

        for name, field in self.fieldByName.iteritems():
            field.resolveLinks()

    def resolvefullPath_(self):
        """Calculate path from root namespace to the current namespace"""
        components = [self.name]
        currentNamespace = self
        while currentNamespace.parentNamespace != None:
            currentNamespace = currentNamespace.parentNamespace
            components.append(currentNamespace.name)

        components.reverse()
        return components

    def importParentNamespaces_(self):
        """All elements of parrent namespaces are visible by default"""
        currentNamespace = self.parentNamespace
        while currentNamespace != None:
            self.importedNamespaces[currentNamespace.fullName] = currentNamespace
            currentNamespace = currentNamespace.parentNamespace
