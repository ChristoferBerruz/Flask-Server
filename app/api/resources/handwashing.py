from flask_restful import Resource, abort, reqparse
from flask import request
from flask_jwt_extended import jwt_required, current_user
from app.database.models import HandwashingRecord, RecordingDevice, Admin
from app.database.schemas import HandwashingRecordSchema
from pony.orm import db_session, ObjectNotFound, select
from datetime import datetime
from marshmallow import ValidationError
import json


record_item_create = HandwashingRecordSchema(exclude=("id", "timestamp"))
record_item_model = HandwashingRecordSchema()
class HandwashingRecordItem(Resource):

    """
    An admin can only access the records for his/her organization
    """
    @jwt_required()
    def get(self, record_id):
        
        admin_id = current_user.id
        try:
            with db_session:
                record = HandwashingRecord[record_id]

                if record.device not in Admin[admin_id].devices:
                    abort(401, message=f'Admins can only access their own records.')
                
                data = {
                    'id':record.id,
                    'timestamp':str(record.timestamp),
                    'duration':record.duration,
                    'device':str(record.device.id)
                }

                return data, 200

        except ObjectNotFound:
            abort(404, message=f'Handwashing record with id {record_id} not found.')


    @jwt_required()
    def put(self):

        data = None
        admin_id = current_user.id
        try:
            data = record_item_create.load(request.json)
        except ValidationError as error:
            abort(400, message=error.messages)


        with db_session:
            
            # Validate that device exists in database
            device_id = data['device']
            device = RecordingDevice.get(id=device_id)
            
            if device is None:
                abort(400, message=f'Device with id {device_id} does not exist in database.')
            
            data['timestamp'] = datetime.now()
            HandwashingRecord(**data)
            return {}, 201


class HandwashingRecords(Resource):

    def get(self, device_id):

        with db_session:
            records = HandwashingRecord.select(lambda r: r.device.id == device_id)

            data = [{
                'id':record.id,
                'timestamp':str(record.timestamp),
                'duration':record.duration,
                'device':str(record.device.id)
            } for record in records]

            return data, 200