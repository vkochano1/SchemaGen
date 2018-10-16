import os

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
          instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


class NamespacePath(object):
    @staticmethod
    def createOutDirectory(prefix, namespace, suffix):
        components = namespace.components
        if components[0] == '':
            components = components[1:]
        dir = os.path.join(prefix, '/'.join(components),  suffix)

        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    @staticmethod
    def componentsFromPath(path):
        return path.split('::')

    @staticmethod
    def componentsToPath(components):
        if components[0] == '':
            components = components[1:]
        return '::'.join(components)

    @staticmethod
    def concatNamespaces(prefix, suffix):
        if prefix == None or prefix == '':
            return suffix
        return prefix + '::' + suffix

    @staticmethod
    def splitFullName(fullName):
        """Splits namespace prefix and element"""
        components = NamespacePath.componentsFromPath(fullName)
        return (components[0:len(components)-1], components[-1])
