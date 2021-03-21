from flask_restful import Resource, abort, reqparse
from flask import request
from app.database.models import HandwashingRecord, RecordingDevice, Admin
from pony.orm import db_session, ObjectNotFound, select
from datetime import datetime
import json
from marshmallow import Schema, fields, ValidationError

class AdminForm(Schema):
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    organization = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


admin_form_validator = AdminForm()

class AdminInfo(Resource):

    def get(self, admin_id):

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


    def post(self):
        try:
            admin_info = admin_form_validator.load(request.json)

            firstname = admin_info['firstname']
            lastname = admin_info['lastname']
            organization = admin_info['organization']
            email = admin_info['email']
            password = admin_info['password']

            with db_session:
                 
                if Admin.get(email=email) is not None:
                    abort(400, message="Admin already exists. Use PATCH to update information")
                
                Admin(
                    firstname = firstname,
                    lastname = lastname,
                    organization = organization,
                    email = email,
                    password = password
                )

                return 201
                
        except ValidationError as error:
            abort(400, message=error.messages)
