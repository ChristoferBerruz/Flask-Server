from flask_restful import Resource, abort, reqparse
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.database.models import HandwashingRecord, RecordingDevice, Admin
from app.database.schemas import AdminSchema
from pony.orm import db_session, ObjectNotFound, select
from datetime import datetime
import json
from marshmallow import Schema, fields, ValidationError

admin_update_info = AdminSchema(only=("firstname", "lastname"), partial=True)
class AdminInfo(Resource):
    
    '''
    Admin can only access the information about itself
    '''
    @jwt_required()
    def get(self):

        admin_id = current_user.id
        try:
            with db_session:
                admin = Admin[admin_id]

                managed_devices = [device.id for device in admin.devices]

                data = {
                    'id':admin.id,
                    'firstname':admin.firstname,
                    'lastname':admin.lastname,
                    'organization':admin.organization,
                    'email':admin.email,
                    'devices':managed_devices
                }
                return data, 200

        except ObjectNotFound:
            abort(404, message=f'Admin of id {admin_id} not found.')

    '''
    All catch to update information about an Admin.
    '''
    @jwt_required()
    def patch(self):

        admin_id = current_user.id
        admin_new_data = None

        try:
            admin_new_data = admin_update_info.load(request.json)
        except ValidationError as error:
            abort(400, message=error.messages)

        with db_session:
            admin = Admin[admin_id]
            admin.set(**admin_new_data)

            return jsonify(message="Sucesfully updated information")
