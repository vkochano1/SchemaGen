import property
import logging
import utils
from common import *

class Message(ModelObject):
    def __init__(self, name, tag, namespace
                , basename = None
                , isAbstract = False
                , isPolymorphic = False
                , usingNamespace = None
                , alias = None
                , displayName = None ):
        super(Message, self).__init__(ObjectType.Message, namespace, name)
        self.className    = name
        self.tag          = tag
        self.basename     = basename
        self.baseMessage  = None
        self.isAbstract    = isAbstract
        self.isPolymorphic = isPolymorphic
        self.usingNamespace = usingNamespace
        self.alias = alias
        self.displayName = displayName
        self.props = []
        self.methods = [];
        self.injections = []
        self.isVector = False
        self.logger.debug("Created message %s::%s(%s)" %(self.namespace.fullName, self.name, str(self.tag)))

    def addMethod(self, method):
        self.methods.append(method)

    def addProperty(self, prop):
        prop.message = self
        self.props.append(prop)

    def countBaseFields(self):
        msg = self.baseMessage
        sum = 0
        while msg != None:
            sum = sum + msg.countFields()
            msg = msg.baseMessage
        return sum

    def countFields(self):
        return len(self.props)

    def countRequiredFields(self):
        return len([prop for prop in self.props if prop.required == True])

    def processInjection(self, name, updated_props):
        addedProps = []
        curMsg = self.namespace.resolveMessageByName(name)
        if not curMsg:
            raise Exception("Failed to resolve injected message %s" % name)
        while curMsg != None:
            curMsg.resolveLinks()

            for prop in reversed(curMsg.props):
                addedProps.append(prop)
            curMsg = curMsg.baseMessage

        updated_props.extend(addedProps[::-1])

    def resolveProp(self, name):
        field = self.namespace.resolveFieldByName(name)
        # fallback to message field
        if field == None:
            field = self.namespace.resolveMessageByName(name)

        return field

    def resolveProps(self):
        updated_props = []
        for prop in self.props:

            if  prop.objectType() == ObjectType.Injection:
                self.processInjection(prop.name, updated_props)
                continue

            if prop.objectType() == ObjectType.VectorProperty:
                self.isVector = True

            field  = self.resolveProp(prop.name)
            if not field and self.usingNamespace != None:
                 field  = self.resolveProp(utils.NamespacePath.concatNamespaces(self.usingNamespace, prop.name))

            if field == None:
                raise Exception("Failed to resolve property %s for message %s" % (prop.name, self.name))

            prop.linkField(field)
            updated_props.append(prop)

        self.props = updated_props

    def resolveBase(self):
        if None == self.basename:
            return None
        resolvedMsg = self.namespace.resolveMessageByName(self.basename)
        if resolvedMsg == None:
            raise Exception('Failed to resolve base class %s' % self.basename)
        return resolvedMsg

    def resolveLinks(self):
        self.baseMessage = self.resolveBase()
        self.resolveProps()

    def __str__(self):
        sprops ='\n[\n' +  '\n,'.join( [ str(prop) for prop in self.props() ]) + '\n]\n'
        smethods = '\n[\n' + ',\n'.join( [ str(method) for method in self.methods ]) + '\n]\n'
        return "\n{\n message:'%s'\n base='%s',\n props:%s,\n is_vector:%s,\n methods:%s\
,\n is_abstract:'%s',\n is_polymorphic:'%s'\n}\n\
        " % (self.namespace.fullName + '::' + self.name
             , str(self.baseMessage), sprops
             , str(self.isVector), smethods
             , str(self.isAbstract), str(self.isPolymorphic))

    def __repr__(self):
        return str(self.__dict__)
