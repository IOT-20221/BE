from main import app, db
from main.common.decorators import jwt_guard, validate_input, check_user_device, check_device_exist, admin_guard, check_user_device_already_exist
from main.models.user import User
from main.models.device import Device
from main.common.exceptions import RecordExistedError, RecordNotFoundError
from main.schemas.device import DeviceSchema
from flask import jsonify, request
from main.libs.mqtt import mqtt_client
import json


@app.get("/device")
@jwt_guard
@admin_guard
def get_devices(*args, **kwargs):
    devices = Device.query.all()
    return DeviceSchema().jsonify(devices, many=True)


@app.get("/device/<string:code>")
@jwt_guard
@check_device_exist
def get_one_device(device, **kwargs):
    return DeviceSchema().jsonify(device)


@app.post("/device")
@validate_input(DeviceSchema, partial=False)
@jwt_guard
@admin_guard
def new_device(code, place_of_manufacture, date_of_manufacture, version, device_name, **kwargs):
    existed = Device.query.filter_by(code=code).one_or_none()
    if existed is not None:
        raise RecordExistedError(error_message=f"Device with such code already existed", error_data={
            "code": code,
        })
    else:
        d = Device()
        d.code = code
        d.date_of_manufacture = date_of_manufacture
        d.place_of_manufacture = place_of_manufacture
        d.device_name = device_name
        d.version = version
        db.session.add(d)
        db.session.commit()
        return DeviceSchema().jsonify(d)


@app.put("/insert-device")
@validate_input(DeviceSchema, partial=True)
@jwt_guard
@check_device_exist
@check_user_device_already_exist
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


@app.post("/device/control/<string:code>")
@jwt_guard
@check_device_exist
@check_user_device
def control_device(user_id, code,  **kwargs):
    topic = f'{code}/control'
    data = request.get_json()
    message = json.dumps(data)
    mqtt_client.publish(topic=topic, payload=message)
    return {}


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
