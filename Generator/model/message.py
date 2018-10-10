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
        self.constructor_body = None;
        self.methods = [];

        self.logger.debug("Created message %s::%s(%s)" %(self.namespace.fullName, self.name, str(self.tag)))

    def addMethod(self, method):
        self.methods.add(method)

    def setConstructorBody(self, constructor_body):
        self.constructor_body = constructor_body

    def addProperty(self, propertyName, required):
        prop = property.Property(self, propertyName,required)
        self.props.append(prop)

    def resolveProps(self):
        for prop in self.props:
            field = self.namespace.resolveFieldByName(prop.name)
            prop.linkField(field)
            self.propertyByName[field.name] = prop

    def resolveBase(self):
        if None == self.basename:
            return None
        return self.namespace.resolveMessageByName(self.basename)

    def resolveLinks(self):
        self.resolveBase()
        self.resolveProps()

    def __str__(self):
        s = '\n'.join( [ str(j) for i, j in self.propertyByName.iteritems() ])
        s = s + '\n'.join( [ str(method) for method in self.methods ])
        return self.namespace.fullName + '::' + self.name + "\n"+ s

    def __repr__(self):
        return str(self.__dict__)
