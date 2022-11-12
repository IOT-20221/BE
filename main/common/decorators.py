import functools
import jwt
from marshmallow import ValidationError
from flask import request
from .exceptions import UnauthorizedError, SchemaValidationError, RecordNotFoundError
from main import app
from main.models.user import User
from main.models.device import Device


# Validate request input with schema
def validate_input(schema, partial: tuple[str] | bool = False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method in ["GET", "DELETE"]:
                data = request.args
            else:
                data = request.get_json()

            try:
                loaded_data = schema().load(data, partial=partial)
            except ValidationError as e:
                raise SchemaValidationError(
                    error_data=e.data, error_message=e.messages
                )
            return func(*args, **loaded_data, **kwargs)

        return wrapper

    return decorator


def jwt_guard(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token_string = request.headers["Authorization"].split(" ")[1]
            header_data = jwt.get_unverified_header(token_string)
            decode_data = jwt.decode(
                token_string,
                key=app.config["JWT_SECRET"],
                algorithms=[header_data["alg"]],
            )
            kwargs["user_id"] = decode_data["user_id"]
        except (jwt.InvalidTokenError, KeyError, IndexError):
            raise UnauthorizedError()
        return func(*args, **kwargs)

    return wrapper


def admin_guard(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs["user_id"]
        user = User.query.get(user_id)
        if not user.is_admin:
            raise UnauthorizedError(
                error_message=["Admin priviledge required for this route"])
        return func(*args, **kwargs)
    return wrapper


def check_user_device(func):
    @functools.wraps(func)
    def wrapper(*args, user_id, code, **kwargs):
        user = User.query.get(user_id)
        filtered = filter(lambda d: d['code'] == 'code', user.devices)
        if filtered is not None and len(filtered) != 0:
            raise UnauthorizedError(
                error_message=["User does not have the authority over this device!"])
        kwargs['user'] = user
        return func(*args, **kwargs)
    return wrapper


def check_device_exist(func):
    @functools.wraps(func)
    def wrapper(*args, code, **kwargs):
        device = Device.query.filter_by(code=code).one_or_none()
        if device is None:
            raise RecordNotFoundError(
                error_message=["No device with such code exists!"])
        kwargs['device'] = device
        kwargs['code'] = code
        return func(*args, **kwargs)
    return wrapper
