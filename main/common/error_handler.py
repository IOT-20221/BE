import http

from flask import jsonify, make_response
from marshmallow import ValidationError

from main import app
from .exceptions import BaseError, SchemaValidationError


def register_error_handler():
    @app.errorhandler(BaseError)
    def handle_base_exception(e):
        return e.to_response()

    @app.errorhandler(SchemaValidationError)
    def handle_schema_validation_error(e: SchemaValidationError):
        return make_response(
            jsonify(
                {
                    "error_message": e.error_message,
                    "error_data": e.error_data,
                }
            )
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return make_response(
            jsonify(
                {
                    "error_message": e.messages,
                    "error_data": e.data,
                }
            ),
            http.HTTPStatus.BAD_REQUEST,
        )

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return make_response(
            jsonify(
                {
                    "error_message": str(e.original_exception),
                }
            ),
            500,
        )

    @app.errorhandler(405)
    def handle_method_not_allow(e):
        return make_response(
            jsonify({"error_message": str(e)}),
            405,
        )

    @app.errorhandler(404)
    def handle_not_found(e):
        return make_response(
            jsonify({"error_message": "NOT FOUND: {}".format(str(e))}), 404
        )
