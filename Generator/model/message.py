import property
import logging

class Message(object):
    def __init__(self, name, tag, namespace, basename = None, Abstract = False,  type = None ):
        self.logger = logging.getLogger(__name__)
        self.name         = name
        self.tag          = tag
        self.type         = type
        self.namespace    = namespace
        self.basename     = basename
        self.baseMessage  = None
        self.propertyByName =  {}
        self.Abstract    = Abstract
        self.props = []
        self.injections = []
        self.constructor_body = None;
        self.methods = [];
        self.isVector = False

        self.logger.debug("Created message %s::%s(%s)" %(self.namespace.fullName, self.name, str(self.tag)))

    def addMethod(self, method):
        self.methods.append(method)

    def setConstructorBody(self, constructor_body):
        self.constructor_body = constructor_body

    def addProperty(self, prop):
        prop.message = self
        self.props.append(prop)

    def processInjection(self, name, updated_props):
        addedProps = []
        curMsg = self.namespace.resolveMessageByName(name)

        while curMsg != None:
            curMsg.resolveLinks()
            for prop in reversed(curMsg.props):
                addedProps.append(prop)
                self.propertyByName[prop.field.name] = prop
            curMsg = curMsg.baseMessage

        updated_props.extend(addedProps[::-1])

    def resolveProps(self):
        updated_props = []
        for prop in self.props:
            if prop.field != None:
                continue

            if prop.isInjection == True:
                self.processInjection(prop.name, updated_props)
                continue

            if prop.isVector == True:
                self.isVector = True

            field = self.namespace.resolveFieldByName(prop.name)
            # fallback to message field
            if field == None:
                field = self.namespace.resolveMessageByName(prop.name)

            prop.linkField(field)
            self.propertyByName[field.name] = prop
            updated_props.append(prop)

        self.props = updated_props

    def resolveBase(self):
        if None == self.basename:
            return None
        return self.namespace.resolveMessageByName(self.basename)

    def resolveLinks(self):
        self.baseMessage = self.resolveBase()
        self.resolveProps()


    def __str__(self):
        s = '\n'.join( [ str(j) for i, j in self.propertyByName.iteritems() ])
        s = s + '\n'.join( [ str(method) for method in self.methods ])
        return self.namespace.fullName + '::' + self.name + "\n"+ s

    def __repr__(self):
        return str(self.__dict__)