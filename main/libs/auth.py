from jwt import encode

from main import app


def generate_token(payload):
    secret = app.config["JWT_SECRET"]
    token = encode(payload=payload, key=secret, algorithm="HS256")
    return token
