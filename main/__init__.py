from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_cors import CORS
from flask_mqtt import Mqtt
from config.base import BaseConfig
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Swagger(app, template={
    "swagger": "2.0",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
        }
    },
    "security":{
        "Bearer": []
    }
})
import main.common
import main.routes
import main.libs.mqtt
from main.common.error_handler import register_error_handler

def register_sub_packages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)


register_error_handler()
register_sub_packages()
