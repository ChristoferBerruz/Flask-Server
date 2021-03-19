from flask_restful import Resource, abort, reqparse
from flask import request
from app.database.models import HandwashingRecord, RecordingDevice, Admin
from pony.orm import db_session, ObjectNotFound
from datetime import datetime
import json


class HandwashingRecordItem(Resource):

    def get(self, record_id):
        
        try:
            with db_session:
                record = HandwashingRecord[record_id]
                data = {
                    'id':record.id,
                    'timestamp':str(record.timestamp),
                    'duration':record.duration,
                    'device':str(record.device.id)
                }

                return data, 200

        except ObjectNotFound:
            abort(404, message=f'Handwashing record with id {record_id} not found.')


    def put(self):
        args = json.loads(request.data)
        device = args.get('device', -1)
        duration = args.get('duration', -1)
        
        if device == -1 or duration == -1:
            abort(404, message=f'You must specify device and duration to create new handwashing record.')

        timestamp = datetime.now()
        with db_session:
            HandwashingRecord(
                timestamp = timestamp,
                duration = duration,
                device = device
            )
            return {}, 201