from .base import BaseSchema
from marshmallow import fields


class ControlSchema(BaseSchema):
    control_code = fields.Int()
