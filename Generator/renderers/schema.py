import utils
import logging
import cogapp
from  model.common import *

class TemplateRouter(object):
    def __init__(self, obj):
        self.modelObj = obj

    def routeObject(self):
        if self.modelObj.objectType() == ObjectType.Message:
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
            for _, enum in namespace.enumerations.iteritems():
                template = TemplateRouter(enum).routeObject()
                genApp.processFile(template, '%s/%s.h' % (dirEnums, enum.name), globals = { 'model' : self.schema, 'enum' : enum, "config":self.cfg })
            for _, field in namespace.fieldByName.iteritems():
                template = TemplateRouter(field).routeObject()
                genApp.processFile(template, '%s/%s.h' % (dirFields, field.name), globals = { 'model' : self.schema, 'field' : field, "config":self.cfg })
