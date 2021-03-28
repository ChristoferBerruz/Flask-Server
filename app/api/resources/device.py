from flask_restful import Resource, abort
from flask import request
from flask_jwt_extended import jwt_required, current_user
from app.database.models import RecordingDevice, Admin
from app.database.schemas import RecordingDeviceSchema
from pony.orm import db_session, ObjectNotFound, select
from datetime import datetime
from marshmallow import ValidationError

device_patch_validator = RecordingDeviceSchema(only=("name", "id"))
class Device(Resource):

    @jwt_required()
    def patch(self):
        admin_id = current_user.id
        data = None

        try:
            data = device_patch_validator.load(request.json)
        except ValidationError as error:
            abort(400, message=error.messages)

        device_id = data['id']
        name = data['name']

        with db_session:

            device = RecordingDevice.get(id = device_id)

            # Verify that this device exists
            if device is None:
                abort(400, message="Device not found in database.")

            # Verify that admin owns the device
            if device_id not in Admin[admin_id].devices.id:
                abort(401, message="The device does not belong to you. Hence, you cannot modify it.")

            # Change name of device
            device.name = name

        