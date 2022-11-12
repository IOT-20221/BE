
from marshmallow import fields, post_load, validate
from .base import BaseSchema


class RecordSchema(BaseSchema):
    id = fields.Integer()
    device_code = fields.String(
        required=True, validate=validate.Length(max=8, min=8))
    data = fields.String(required=True)

    @post_load
    def check_code(self, data, **kwargs):
        if 'device_code' in data:
            data['device_code'] = data['device_code'].strip()
        return data
