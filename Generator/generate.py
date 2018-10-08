import __future__

import os
import loader.to_model
import loader.environment
import loader.data_type
import cogapp
import logging

format = '%(name)s:%(levelname)-8s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format = format)
genApp = cogapp.Cog()
genApp.options.bDeleteCode = True
env = loader.environment.Environment()
env.addIncludePath('./')
env.addIncludePath('./test')

l = loader.data_type.Loader()
model = loader.to_model.ModelLoader('test/data.xml',env).modelNamespaces

for _, namespace in model.namespaces.iteritems():
    for _, message in namespace.messagesByName.iteritems():
        genApp.processFile("templates/message.cog", 'test/out/Messages/%s.h' % message.name, globals = { 'model' : model, 'msg' : message })
    for _, enum in namespace.enumerations.iteritems():
        genApp.processFile("templates/enum.cog", 'test/out/Enumerations/%s.h' % enum.name, globals = { 'model' : model, 'enum' : enum })
    for _, field in namespace.fieldByName.iteritems():
        genApp.processFile("templates/field.cog", 'test/out/Fields/%s.h' % field.name, globals = { 'model' : model, 'field' : field })
