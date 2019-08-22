from backend.api import ModelSerializer, fields
from backend.database import Model
from backend.extensions.api import api
from backend.extensions.marshmallow import Schema


class ErrorSerializer(Schema):
    message = fields.String(required=True)
