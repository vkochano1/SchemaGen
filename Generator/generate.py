import __future__

import os
import loader.to_model
import loader.environment
import loader.data_type
import cogapp
import logging
import utils

genApp = cogapp.Cog()
genApp.options.bDeleteCode = True
env = loader.environment.Environment()
env.addIncludePath('./')
env.addIncludePath('./test')

class Config(object):
    def __init__(self):
        self.REVISION = "1234"
        format = '%(name)-20s:%(levelname)-8s: %(message)s'
        logging.basicConfig(level=logging.DEBUG, format = format)

    def needToRenderNamespace(self, namespace):
        return not namespace.fullName.startswith("Z::F")

cfg = Config()
l = loader.data_type.Loader()
model = loader.to_model.ModelLoader('test/data.xml',env).modelNamespaces

prefix = 'test/out/'

for _, namespace in model.namespaces.iteritems():

    if not namespace.hasElements() or not cfg.needToRenderNamespace(namespace):
        continue

    dirMsgs = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Messages' );
    dirEnums = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Enumerations' );
    dirFields = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Fields' );

    for _, message in namespace.messagesByName.iteritems():
        genApp.processFile("templates/message.cog", '%s/%s.h' % (dirMsgs, message.name), globals = { 'model' : model, 'msg' : message, "config":cfg })
    for _, enum in namespace.enumerations.iteritems():
        genApp.processFile("templates/enum.cog", '%s/%s.h' % (dirEnums, enum.name), globals = { 'model' : model, 'enum' : enum, "config":cfg })
    for _, field in namespace.fieldByName.iteritems():
        genApp.processFile("templates/field.cog", '%s/%s.h' % (dirFields, field.name), globals = { 'model' : model, 'field' : field, "config":cfg })
