from flask import request, jsonify
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.database.schemas import AdminSchema
from app.database.models import Admin
from marshmallow import ValidationError
from pony.orm import db_session

login_data_validator = AdminSchema(only=("email", "password"))

class Login(Resource):

    def post(self):

        try:
            data_json = login_data_validator.load(request.json)

            email = data_json['email']
            password = data_json['password']

            with db_session:
                admin = Admin.get(email=email, password=password)

                if admin is None:
                    return {"message": "Invalid credentials."}, 401

                access_token = create_access_token(identity = admin.id)
                return {"access_token":access_token}

        except ValidationError as error:
            abort(400, message=error.messages)

