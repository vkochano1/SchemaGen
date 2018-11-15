import utils
import logging
import cogapp
from  model.common import *
import renderers.router

class Renderer(object):
    def __init__(self, schema, config):
        self.schema = schema
        self.cfg = config
        self.genApp = cogapp.Cog()
        self.genApp.options.bDeleteCode = True

    def renderGroup(self, groupName, namespace, router, objectsByName):
        if len(objectsByName) == 0:
            return

        prefix = self.cfg.outDir

        dir = utils.NamespacePath.createOutDirectory(prefix, namespace, groupName);

        groupTemplate = None
        objectGroupNameInTemplate = None

        for _, obj in objectsByName.iteritems():
            template = router.routeObject(obj)

            if groupTemplate == None:
                groupTemplate = router.routeGroupObject(obj)
                objectGroupNameInTemplate = router.objectGroupNameInTemplate(obj)

            globals = { 'model' : self.schema
                      , router.objectNameInTemplate(obj) : obj
                      , "config": self.cfg
                      }

            self.genApp.processFile(template
                                    , "%s/%s.h" % (dir, obj.name)
                                    , globals = globals)

        objs = objectsByName.values ()

        self.genApp.processFile(groupTemplate
                                , "%s/../%s.h" % (dir, groupName)
                                , globals = { 'model' : self.schema
                                            , objectGroupNameInTemplate : objs
                                            , "config": self.cfg
                                            }
                                )

    def render(self):
        for _, namespace in self.schema.namespaces.iteritems():
            if not namespace.hasElements() or not self.cfg.needToRenderNamespace(namespace):
                continue
            self.renderGroup("Messages", namespace, renderers.router.TemplateRouter, namespace.messagesByName)
            self.renderGroup("Enumerations", namespace, renderers.router.TemplateRouter, namespace.enumerations)
            self.renderGroup("Fields", namespace, renderers.router.TemplateRouter, namespace.fieldByName)
            self.renderGroup("Payloads", namespace, renderers.router.TemplateRouter, namespace.payloadsByName)
            self.renderGroup("Configurations", namespace, renderers.router.TemplateRouter, namespace.configurationsByName)
