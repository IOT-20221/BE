from main import app, db
from main.models.user import User
from main.common.exceptions import UnauthorizedError, RecordNotFoundError, RecordExistedError
from main.common.decorators import validate_input, jwt_guard, admin_guard
from main.schemas.user import UserSchema
from main.libs.auth import generate_token
from flask import jsonify


@app.post("/user/sign-in")
@validate_input(UserSchema)
def sign_in(username, password, **kwargs):
    user = User.query.filter_by(username=username).one_or_none()
    if user is not None:
        if not user.check_password(password=password):
            raise UnauthorizedError()
        else:
            return jsonify({"access_token": generate_token({"user_id": user.id})})
    else:
        raise RecordNotFoundError()


@app.post("/user/sign-up")
@validate_input(UserSchema, partial=True)
def sign_up(username, password, **kwargs):
    existing_user_name = User.query.filter_by(username=username).one_or_none()
    if existing_user_name is not None:
        raise RecordExistedError(
            error_message="Username {} has already been used".format(username)
        )

    new_user = User()
    new_user.username = username
    new_user.set_password(password)
    new_user.is_admin = False
    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {
            "user_id": new_user.id,
            "access_token": generate_token({"user_id": new_user.id}),
        }
    )


@app.post("/user/me")
@jwt_guard
def test_user(user_id, **kwargs):
    user = User.query.get(user_id)
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "is_admin":  user.is_admin
    })


@app.post("/user/me-admin")
@jwt_guard
@admin_guard
def test_admin(user_id, **kwargs):
    user = User.query.get(user_id)
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin
    })
