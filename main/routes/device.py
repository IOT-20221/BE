from main import app, db
from main.common.decorators import jwt_guard, validate_input, check_user_device, check_device_exist
from main.models.user import User
from main.models.device import Device
from main.common.exceptions import RecordExistedError, RecordNotFoundError
from main.schemas.device import DeviceSchema
from flask import jsonify
from main.libs.mqtt import mqtt_client


@app.post("/device")
@validate_input(DeviceSchema, partial=True)
@jwt_guard
@check_device_exist
def add_device_to_user(user_id, device, **kwargs):
    user = User.query.get(user_id)
    user.devices.append(device)
    db.session.commit()
    mqtt_client.subscribe(f'{device.code}/data')
    devices = DeviceSchema().dump(user.devices, many=True)
    return jsonify({
        'user_id': user.id,
        'devices': devices
    })


@app.delete("/device/<string:code>")
@validate_input(DeviceSchema, partial=True)
@jwt_guard
def remove_device(user_id, code, **kwargs):
    user = User.query.get(user_id)

    filtered = list(filter(lambda d: d.code != code, user.devices))
    user.devices = filtered
    db.session.commit()
    devices = DeviceSchema().dump(user.devices, many=True)
    mqtt_client.unsubscribe(f'{code}/data')
    return jsonify({
        'user_id': user.id,
        'devices': devices
    })
