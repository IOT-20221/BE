import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get("JWT_SECRET")
    PER_PAGE = int(os.environ.get("PER_PAGE")) | 5
    MQTT_BROKER_URL=os.environ.get("MQTT_BROKER_URL")
    MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT"))
    MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
    MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
    
