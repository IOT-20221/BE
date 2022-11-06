from marshmallow import fields

from .base import BaseSchema


class ErrorSchema(BaseSchema):
    error_message = fields.List(fields.String())
    error_data = fields.Raw()
    error_code = fields.Integer()