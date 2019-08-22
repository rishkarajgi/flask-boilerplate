import json
from urllib.parse import urlparse

from flask import Response, url_for
from flask.testing import FlaskClient
from werkzeug.utils import cached_property


class HtmlTestClient(FlaskClient):
    token = None

    def open(self, *args, **kwargs):
        kwargs.setdefault('headers', {})
        if self.token:
            kwargs['headers']['Authentication-Token'] = self.token
        return super().open(*args, **kwargs)


class ApiTestClient(HtmlTestClient):
    def open(self, *args, **kwargs):
        kwargs['data'] = json.dumps(kwargs.get('data'))

        kwargs.setdefault('headers', {})
        kwargs['headers']['Content-Type'] = 'application/json'
        kwargs['headers']['Accept'] = 'application/json'

        return super().open(*args, **kwargs)


class HtmlTestResponse(Response):
    @cached_property
    def scheme(self):
        return urlparse(self.location).scheme

    @cached_property
    def netloc(self):
        return urlparse(self.location).netloc

    @cached_property
    def path(self):
        return urlparse(self.location).path

    @cached_property
    def params(self):
        return urlparse(self.location).params

    @cached_property
    def query(self):
        return urlparse(self.location).query

    @cached_property
    def fragment(self):
        return urlparse(self.location).fragment

    @cached_property
    def html(self):
        return self.data.decode('utf-8')


class ApiTestResponse(HtmlTestResponse):
    @cached_property
    def json(self):
        assert self.mimetype == 'application/json', (self.mimetype, self.data)
        return json.loads(self.data)

    @cached_property
    def errors(self):
        return self.json.get('errors', {})
