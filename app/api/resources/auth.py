from flask import request, jsonify
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt, current_user
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
from app.database.schemas import AdminSchema, PasswordUpdateForm
from app.database.models import Admin
from marshmallow import ValidationError
from pony.orm import db_session

from werkzeug.security import generate_password_hash, check_password_hash
from app.cache import CacheServices
from datetime import timedelta, datetime, timezone

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

                access_token = create_access_token(identity = admin)

                response = jsonify(msg="Login successful")
                set_access_cookies(response, access_token)

                return response
                

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


# Time to remove the token from the blacklist
ACCESS_EXPIRES = timedelta(hours=1)
class Logout(Resource):

    @jwt_required()
    def post(self):
        jwt_redis_blocklist = CacheServices.get_redis_service('jwt_redis_blocklist')
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        response =  jsonify(msg="Logout successful")
        unset_jwt_cookies(response)
        return response


password_update_validator = PasswordUpdateForm()
class UpdatePassword(Resource):
    
    @jwt_required()
    def post(self):
        admin_id = current_user.id

        update_data = None
        
        try:
            update_data = password_update_validator.load(request.json)
        except ValidationError as error:
            abort(400, message=error.messages)

        with db_session:
            admin = Admin[admin_id]

            valid_password = check_password_hash(admin.password, update_data['current_password'])

            if not valid_password:
                abort(400, message="Current password is incorrect. Try again.")
            
            admin.password = generate_password_hash(update_data['new_password'])

            return jsonify(message = "Sucesfully update your password.")


def add_automatic_token_refresh(app):

    @app.after_request
    def refresh_token(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)

            expires_in = 30

            # Check if token expires in given timedelta
            target_timestamp = datetime.timestamp(now + timedelta(minutes=expires_in))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
                
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original respone
            return response