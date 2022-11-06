import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get("JWT_SECRET")
    PER_PAGE = int(os.environ.get("PER_PAGE")) | 5
