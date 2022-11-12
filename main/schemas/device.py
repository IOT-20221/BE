from .base import BaseSchema
from marshmallow import fields, validate, post_load
from .user import UserSchema


class DeviceSchema(BaseSchema):
    id = fields.Integer()
    code = fields.String(
        required=True, validate=validate.Length(max=8, min=8))
    device_name = fields.String(
        required=True, validate=validate.Length(max=255)
    )
    date_of_manufacture = fields.String(
        required=True, validate=validate.Length(max=255))
    place_of_manufacture = fields.String(
        required=True, validate=validate.Length(max=255))
    version = fields.String(required=True, validate=validate.Length(max=10))
    users = fields.List(fields.Nested(UserSchema(), exclude=("devices",)))

    @post_load
    def strip(self, data, **kwargs):
        if "code" in data:
            data['code'] = data['code'].strip()
        if 'device_name' in data:
            data['device_name'] = data['device_name'].strip()
        if 'date_of_manufacture' in data:
            data['date_of_manufacture'] = data['date_of_manufacture'].strip()
        if 'place_of_manufacture' in data:
            data['place_of_manufacture'] = data['place_of_manufacture'].strip()
        if 'version' in data:
            data['version'] = data['version'].strip()
        return data
