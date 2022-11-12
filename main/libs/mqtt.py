from main.models.record import Record
from main.models.device import Device
from main import app, db
from flask_mqtt import Mqtt
import re

mqtt_client = Mqtt()


@mqtt_client.on_connect()
def on_connection(client, userdata, flags, rc):
    if rc == 0:
        print("Connected sucessfully to MQTT Broker!")
        # with app.app_context():
        #     devices = Device.query.filter(
        #         Device.users.query.count() != 0).all()
        #     for d in devices:
        #         mqtt_client.subscribe(f'{d.code}/data')
    else:
        print(f"Failed to connect to MQTT broker with status {rc}")


@mqtt_client.on_message()
def on_message(client, userdata, message):
    with app.app_context():
        topic = message.topic
        payload = message.payload.decode()
        if re.search('/data$', topic):
            s = Record()
            s.data = payload
            code = topic.split('/')[0]
            s.device_code = code
            db.session.add(s)
            db.session.commit()
        else:
            return


mqtt_client.init_app(app)
