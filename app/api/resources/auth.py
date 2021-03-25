from flask import request, jsonify
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.database.schemas import AdminSchema
from app.database.models import Admin
from marshmallow import ValidationError
from pony.orm import db_session

from werkzeug.security import generate_password_hash, check_password_hash

login_data_validator = AdminSchema(only=("email", "password"))

class Login(Resource):

    def post(self):

        try:
            data_json = login_data_validator.load(request.json)

            email = data_json['email']
            password = data_json['password']
            with db_session:
                admin = Admin.get(email=email)

                if admin is None:
                    abort(400, message="Email is not registered.")

                if not check_password_hash(admin.password, password):
                    abort(400, message="Invalid password.")

                access_token = create_access_token(identity = admin.id)
                return {"access_token":access_token}

        except ValidationError as error:
            abort(400, message=error.messages)


# For an Admin to register, there is no need for 
# and ID nor devices
sign_up_validator = AdminSchema(exclude=("id", "devices"))
class SignUp(Resource):

    """
    Adds an admin to the admin database. Payload is read from JSON body
    of the request.
    """
    def post(self):

        try:
            data_json = sign_up_validator.load(request.json)

            email = data_json['email']

            with db_session:

                # Check if user exists in database
                admin = Admin.get(email = email)

                # Admin already exists
                if admin is not None:
                    abort(400, message = "You are already signed up. Login instead")
                
                # Hashing password
                data_json['password'] = generate_password_hash(data_json['password'])

                # Create record
                Admin(**data_json)

                return {"message": "Sucesfully created admin"}, 201
        
        except ValidationError as error:
            abort(400, message=error.messages)