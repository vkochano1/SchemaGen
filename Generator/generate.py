import __future__

import os
import loader.schema
import loader.environment
import loader.data_type
import loader.project
import cogapp
import logging
import utils

genApp = cogapp.Cog()
genApp.options.bDeleteCode = True

project = loader.project.Loader('project.xml')
project.load()
schemaLoader, cfg = project.schemas[0]
schemaLoader.load()
model = schemaLoader.schema

for _, namespace in model.namespaces.iteritems():

    if not namespace.hasElements() or not cfg.needToRenderNamespace(namespace):
        continue

    prefix = cfg.outDir
    dirMsgs = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Messages' );
    dirEnums = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Enumerations' );
    dirFields = utils.NamespacePath.createOutDirectory(prefix, namespace, 'Fields' );

    for _, message in namespace.messagesByName.iteritems():
        genApp.processFile("templates/message.cog", '%s/%s.h' % (dirMsgs, message.name), globals = { 'model' : model, 'msg' : message, "config":cfg })
    for _, enum in namespace.enumerations.iteritems():
        genApp.processFile("templates/enum.cog", '%s/%s.h' % (dirEnums, enum.name), globals = { 'model' : model, 'enum' : enum, "config":cfg })
    for _, field in namespace.fieldByName.iteritems():
        genApp.processFile("templates/field.cog", '%s/%s.h' % (dirFields, field.name), globals = { 'model' : model, 'field' : field, "config":cfg })
