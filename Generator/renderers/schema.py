import utils
import logging
import cogapp
from  model.common import *

class TemplateRouter(object):
    def __init__(self, obj):
        self.modelObj = obj

    def routeObject(self):
        if self.modelObj.objectType() == ObjectType.Message:
            if self.modelObj.isVector == True:
                return "templates/message_vector.cog"
            if self.modelObj.countFields() == 0:
                return "templates/message_no_props.cog"
            else:
                return "templates/message.cog"
        elif self.modelObj.objectType() == ObjectType.Field:
            return "templates/field.cog"
        elif self.modelObj.objectType() == ObjectType.Enumeration:
            return "templates/enum.cog"


class Renderer(object):
    def __init__(self, schema, config):
        self.schema = schema
        self.cfg = config

    def render(self):
        genApp = cogapp.Cog()
        genApp.options.bDeleteCode = True

        for _, namespace in self.schema.namespaces.iteritems():
            if not namespace.hasElements() or not self.cfg.needToRenderNamespace(namespace):
                continue

            prefix = self.cfg.outDir
            dirMsgs = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Messages' );
            dirEnums = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Enumerations' );
            dirFields = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Fields' );

            for _, message in namespace.messagesByName.iteritems():
                template = TemplateRouter(message).routeObject()
                genApp.processFile(template, '%s/%s.h' % (dirMsgs, message.name), globals = { 'model' : self.schema, 'msg' : message, "config": self.cfg })

            messages = [message for message in namespace.messagesByName.values ()]
            if len(messages) > 0:
                genApp.processFile("templates/messages.cog", '%s/../Messages.h' % (dirMsgs), globals = { 'model' : self.schema, 'msgs' : messages, "config": self.cfg })

            for _, enum in namespace.enumerations.iteritems():
                template = TemplateRouter(enum).routeObject()
                genApp.processFile(template, '%s/%s.h' % (dirEnums, enum.name), globals = { 'model' : self.schema, 'enum' : enum, "config":self.cfg })

            enumerations = [enumeration for _, enumeration in namespace.enumerations.iteritems()]
            if len(enumerations) > 0:
                genApp.processFile("templates/enums.cog", '%s/../Enumerations.h' % (dirMsgs), globals = { 'model' : self.schema, 'enums' : enumerations, "config": self.cfg })

            for _, field in namespace.fieldByName.iteritems():
                template = TemplateRouter(field).routeObject()
                genApp.processFile(template, '%s/%s.h' % (dirFields, field.name), globals = { 'model' : self.schema, 'field' : field, "config":self.cfg })

            fields = [field for field in namespace.fieldByName.values ()]
            if len(fields) > 0:
                genApp.processFile("templates/fields.cog", '%s/../Fields.h' % (dirMsgs), globals = { 'model' : self.schema, 'fields' : fields, "config": self.cfg })
