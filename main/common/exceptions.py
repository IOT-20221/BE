
from http import HTTPStatus

from flask import make_response

from main.schemas.error import ErrorSchema


class BaseError(Exception):
    def __init__(
        self,
        *,
        error_message=None,
        error_data=None,
        status_code: int | None = None,
    ):
        if error_message is not None:
            self.error_message = error_message
        if status_code is not None:
            self.status_code = status_code
        self.error_data = error_data

    def to_response(self):
        response = ErrorSchema().jsonify(self)
        return make_response(response, self.status_code)


class SchemaValidationError(BaseError):
    status_code = HTTPStatus.BAD_REQUEST
    error_message = ["Fail to validate schema."]


class RecordExistedError(BaseError):
    status_code = HTTPStatus.BAD_REQUEST
    error_message = ["Record already existed."]


class RecordNotFoundError(BaseError):
    status_code = HTTPStatus.NOT_FOUND
    error_message = ["Record does not exist."]


class UnauthorizedError(BaseError):
    status_code = HTTPStatus.UNAUTHORIZED
    error_message = ["Fail to authorize user."]


class ForbiddenAccessError(BaseError):
    status_code = HTTPStatus.FORBIDDEN
    error_message = ["The queried resources are forbidden"]
