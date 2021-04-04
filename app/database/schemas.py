# Schemas representation of the database models
# to be used across the program

from marshmallow import Schema, fields, ValidationError
from datetime import datetime

class AdminSchema(Schema):
    id = fields.Integer(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    organization = fields.Str(required=True)
    email = fields.Email(required=True)
    devices = fields.List(fields.Integer())
    password = fields.Str(required=True)

class RecordingDeviceSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    location = fields.Str()
    date_installed = fields.DateTime()
    admin = fields.Integer()

class HandwashingRecordSchema(Schema):
    id = fields.Integer()
    timestamp = fields.DateTime()
    duration = fields.Float()
    device = fields.Integer()

class PasswordUpdateForm(Schema):
    current_password = fields.Str()
    new_password = fields.Str()

class AllRecordParameters(Schema):
    device_id = fields.Integer()
    start_date = fields.DateTime()
    end_date = fields.DateTime()