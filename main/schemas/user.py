from .base import BaseSchema
from marshmallow import fields, validate, ValidationError, validates
# from .device import DeviceSchema


class UserSchema(BaseSchema):
    id = fields.Integer()
    username = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    is_admin = fields.Boolean()
    devices = fields.List(fields.Nested(
        "DeviceSchema", exclude=('users',)), allow_none=True)

    @validates("password")
    def password_validator(self, value: str):
        has_upper = False
        has_lower = False
        has_number = False
        has_non_ascii = False
        errors = []

        for char in value:
            if char.isupper():
                has_upper = True
            if char.islower():
                has_lower = True
            if char.isnumeric():
                has_number = True
            if not char.isascii():
                has_non_ascii = True

        if has_non_ascii:
            errors.append("Password contains special characters")
        if not has_upper:
            errors.append("Password must contain upper characters")
        if not has_lower:
            errors.append("Password must contain lower characters")
        if not has_number:
            errors.append("Password must contain numeric characters")
        if len(errors) > 0:
            raise ValidationError(message=errors)
