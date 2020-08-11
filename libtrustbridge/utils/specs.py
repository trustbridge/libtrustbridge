from apispec.exceptions import OpenAPIError
from apispec.utils import validate_spec
from flask_script import Command, Option


def register_specs(app, spec, views):
    for view in app.view_functions.values():
        if view.__name__ in views:
            spec.path(view=view, app=app)
    app.config['spec'] = spec


class GenerateApiSpecCommand(Command):
    """
    Generate api spec
    """

    def __call__(self, app=None, *args, **kwargs):
        self.spec = app.config['spec']

        return super().__call__(app, *args, **kwargs)

    def get_options(self):
        return (
            Option('-f', '--filename',
                   dest='filename',
                   default='swagger.yaml',
                   help='save generated spec into file'),
        )

    def run(self, filename):
        try:
            validate_spec(self.spec)
        except OpenAPIError as e:
            print(f'API spec is not valid')
            print(e)
            exit(1)

        with open(filename, 'w') as fp:
            fp.write(self.spec.to_yaml())

        print(f'API spec has been written into {filename}')
