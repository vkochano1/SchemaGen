import __future__

import loader.schema
import loader.environment
import loader.datatype
import loader.project
import renderers.schema

project = loader.project.Loader('project.xml')
project.load()

for schemaLoader, cfg in project.schemas:
    schemaLoader.load()
    renderer = renderers.schema.Renderer(schemaLoader.schema, cfg)
    renderer.render()
