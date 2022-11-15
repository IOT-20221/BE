from main import app, db
from main.common.decorators import jwt_guard, validate_input, check_user_device, check_device_exist, admin_guard, check_user_device_already_exist
from main.models.user import User
from main.models.device import Device
from main.common.exceptions import RecordExistedError, RecordNotFoundError
from main.schemas.device import DeviceSchema
from main.schemas.control import ControlSchema
from flask import jsonify
from main.libs.mqtt import mqtt_client
import json


@app.post("/device")
@validate_input(DeviceSchema, partial=False)
@jwt_guard
@admin_guard
def new_device(code, place_of_manufacture, date_of_manufacture, version, device_name, **kwargs):
    """
    Create a new device.
    This route is protected and can only be used with a admin token
    ---
    tags:
      - device
    security:
      - bearerAuth: [admin]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Device
          required:
            - code
            - device_name
            - date_of_manufacture
            - place_of_manufacture
          properties:
            code:
              type: string
              description: The device's code 8 characters string.
            device_name:
              type: string
              description: name of the device
            date_of_manufacture:
              type: string
              format: date-time
              description: date of manufacture
            place_of_manufacture:
              type: string
              description: place of manufacture
            version:
              type: string
              description: version of the device
              default: "1.0.0"
    responses:
      200:
        description: Created
        schema:
          $ref: '#/definitions/Device'
      400:
        description: Device with that code already existed or invalid json body
      401:
        description: Unauthorized
    """
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


@app.put("/device")
@validate_input(DeviceSchema, partial=True)
@jwt_guard
@check_device_exist
@check_user_device_already_exist
def add_device_to_user(user_id, device, **kwargs):
    """
    User register a new device
    This route is protected and can only be used with a user token
    ---
    tags:
      - device
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - code
          properties:
            code:
              type: string
              description: The device's code 6 characters string.
    responses:
      200:
        description: OK
      400:
        description: Device with that code already  registerd to that user, or device with that code does not exist
      401:
        description: Unauthorized
    """
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
@validate_input(ControlSchema)
def control_device(user_id, code, control_code, **kwargs):
    topic = f'{code}/control'
    message = json.dumps({"control_code": control_code})
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
