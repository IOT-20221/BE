from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

from config.base import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import main.common
import main.routes
from main.common.error_handler import register_error_handler

def register_sub_packages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)


register_error_handler()
register_sub_packages()
