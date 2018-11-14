import namespace
import utils

class Schema(object):
    def __init__(self):
        self.namespaces = {'': namespace.Namespace('', None) }

    def createSubNamespaces(self, path, parent):
        namespace = parent
        createdNamespaces = []
        for component in path:
            parentNamespace = namespace
            namespace = None
            if parentNamespace == None:
                namespace = namespace.Namespace(component, None)
            else:
                namespace = parentNamespace.addSubNamespace(component)

            createdNamespaces.append(namespace)
            self.namespaces[namespace.fullName] = namespace

        return createdNamespaces

    def createOrGet(self, namespaceName):
        components = utils.NamespacePath.componentsFromPath(namespaceName)
        currentPathComponents = []
        parentNamespace = self.namespaces['']
        namespace = parentNamespace
        for component in components:
            currentPathComponents.append(component)
            pathStr = utils.NamespacePath.componentsToPath(currentPathComponents)
            parentNamespace = namespace
            namespace = self.namespaces.get(pathStr)

            if None == namespace:
                suffixPath = components[len(currentPathComponents)-1:]
                createdNamespaces = self.createSubNamespaces(suffixPath, parentNamespace)
                return createdNamespaces

        return [namespace]

    def resolveLinks(self):
        # All import namespaces must be resolved b4
        # field/message resolution step
        for _, namespace in self.namespaces.iteritems():
            namespace.resolveImports(self.namespaces)

        for _, namespace in self.namespaces.iteritems():
            namespace.resolveLinks(self.namespaces)
