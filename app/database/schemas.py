# Schemas representation of the database models
# to be used across the program

from marshmallow import Schema, fields, ValidationError

class AdminSchema(Schema):
    id = fields.Integer()
    firstname = fields.Str()
    lastname = fields.Str()
    organization = fields.Str()
    email = fields.Email()
    devices = fields.List(fields.Integer())
    password = fields.Str()

class RecordingDeviceSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    location = fields.Str()
    date_installed = fields.DateTime()
    admin = fields.Integer()

class HanwashingRecordSchema(Schema):
    id = fields.Integer()
    timestamp = fields.DateTime()
    duration = fields.Float()
    device = fields.Integer()

class PasswordUpdateForm(Schema):
    current_password = fields.Str()
    new_password = fields.Str()