import __future__
import argparse

import loader.schema
import loader.environment
import loader.datatype
import loader.project
import renderers.schema



def generate(project, onlyLoad):
    project = loader.project.Loader(project)
    project.load()

    for schemaLoader, cfg in project.schemas:
        schemaLoader.load()
        if not onlyLoad:
            renderer = renderers.schema.Renderer(schemaLoader.schema, cfg)
            renderer.render()


parser = argparse.ArgumentParser(description='Generates schema from XML')

parser.add_argument('action', choices = ['gen', 'load'], help="""gen  -> generate the schema
                                                            , load -> only validates the schema""")
parser.add_argument('project', help="""The project file path""")

parser.add_argument('--skipNamespaces', default='',
                    help='comma separated list of namespaces to be excluded from render set')

args = parser.parse_args()

generate(args.project, args.action == 'load')
