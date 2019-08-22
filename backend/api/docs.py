import types

from flask_apispec import (FlaskApiSpec, MethodResource, ResourceMeta, doc,
                           marshal_with, use_kwargs, utils)
from flask_apispec.apidoc import ResourceConverter, ViewConverter
from flask_apispec.extension import make_apispec

from .constants import CREATE, GET, LIST, POST
from .utils import get_last_param_name


class CustomApiSpec(FlaskApiSpec):
    def init_app(self, app):
        self.app = app
        self.spec = self.app.config.get('APISPEC_SPEC') or \
            make_apispec(self.app.config.get('APISPEC_TITLE', 'base-flask-api'),
                         self.app.config.get('APISPEC_VERSION', 'v1'),
                         self.app.config.get('APISPEC_OAS_VERSION', '2.0'))
        self.add_swagger_routes()
        self.resource_converter = CustomResourceConverter(
            self.app, spec=self.spec)
        self.view_converter = CustomViewConverter(app=self.app, spec=self.spec)

        for deferred in self._deferred:
            deferred()

    def register(self, target=None, endpoint=None, blueprint=None,
                 resource_class_args=None, resource_class_kwargs=None):
        if target is None and endpoint in self.app.view_functions:
            resource = self.app.view_functions[endpoint]
            target = resource
        if hasattr(target, 'view_class'):
            target = getattr(target, 'view_class')
        super().register(target, endpoint, blueprint,
                         resource_class_args, resource_class_kwargs)


class CustomResourceConverter(ResourceConverter):

    def get_operations(self, rule, resource):
        operations = {}
        for method in rule.methods:
            method_name = method.lower()
            if method_name != 'options':
                has_last_param = get_last_param_name(rule.rule)
                if has_last_param:
                    operations[method] = self.get_method(
                        rule, resource, method_name)
                else:
                    if method_name == POST:
                        operations[method] = self.get_method(
                            rule, resource, CREATE)
                    elif method_name == GET:
                        operations[method] = self.get_method(
                            rule, resource, LIST)
                    else:
                        operations[method] = self.get_method(
                            rule, resource, method_name)
        return operations

    def get_method(self, rule, resource, method_name):
        method = types.SimpleNamespace()  # getattr(resource, method_name, None) or
        doc_decorators = getattr(resource, 'doc_decorators', None) or {}
        for decorator in (doc_decorators.get(method_name) or []):
            method = decorator(method)
        return method


class CustomViewConverter(ViewConverter):

    def get_operations(self, rule, view):
        return {
            method: view
            for method in rule.methods
            if method.lower() != 'options'
        }


jwt_authorization = {
    'Authorization': {
        'description':
        'Authorization HTTP header with JWT token, like: Authorization: Bearer asdf.qwer.zxcv',
        'in':
        'header',
        'type':
        'string',
        'required':
        False
    }
}
