import utils
import logging
import cogapp

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
                genApp.processFile("templates/message.cog", '%s/%s.h' % (dirMsgs, message.name), globals = { 'model' : self.schema, 'msg' : message, "config": self.cfg })
            for _, enum in namespace.enumerations.iteritems():
                genApp.processFile("templates/enum.cog", '%s/%s.h' % (dirEnums, enum.name), globals = { 'model' : self.schema, 'enum' : enum, "config":self.cfg })
            for _, field in namespace.fieldByName.iteritems():
                genApp.processFile("templates/field.cog", '%s/%s.h' % (dirFields, field.name), globals = { 'model' : self.schema, 'field' : field, "config":self.cfg })
