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
    """
    Authenticate use
    ---
    tags:
      - authentication
    description: Authenticate a user with given credentials
    parameters:
      - name: body
        in: body
        schema: 
          properties:
            username:
              type: string
              description: username
            password:
              type: string
              description: password, must contain both numeric and non-numeric characters, be at least 6 characters long, contain both lower and upper case characters, and must not contain any non alphanumberic characters
        required: true
    responses:
      200:
        description: OK.
      400:
        description: password is invalid 
      401:
        description: username and password does not match
      404:
        description: no user with that username

    """
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
    """
    User sign-up method.
    ---
    tags:
      - authentication
    description: Sign up an user
    parameters:
      - name: body
        in: body
        schema: 
          properties:
            username:
              type: string
              description: username
            password:
              type: string
              description: password, must contain both numeric and non-numeric characters, be at least 6 characters long, contain both lower and upper case characters, and must not contain any non alphanumberic characters
        required: true
    responses:
      200:
        description: User successfully sign up.
      400:
        description: Bad request, username already exist, or password is invalid 
    """
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
def user_info(user_id, **kwargs):
    user = User.query.get(user_id)
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "is_admin":  user.is_admin
    })


@app.post("/user/admin/me")
@jwt_guard
@admin_guard
def test_admin(user_id, **kwargs):
    user = User.query.get(user_id)
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin
    })
