from marshmallow import Schema, fields, EXCLUDE, validate
from flask import jsonify


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()


class PageSchema(BaseSchema):
    page = fields.Integer(required=True, validate=validate.Range(min=0))