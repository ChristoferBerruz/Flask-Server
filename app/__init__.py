from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Api
from app.api.resources.handwashing import HandwashingRecordItem, HandwashingRecords
from app.api.resources.admin import AdminInfo
from app.api.resources.auth import Login, SignUp, Logout, UpdatePassword
from flask_jwt_extended import JWTManager

from app.database.models import db
from app.config import config

from app.utils.callbacks import JWTCallbacks
from app.cache import CacheServices

# Create flask app
app = Flask(__name__)

app.config.from_object(config)

# Add auth service
jwt = JWTManager(app)

# Create a cache service
CacheServices.create_redis_service(
    service_key = 'jwt_redis_blocklist',
    host = config.REDIS_HOST,
    db = 0,
    decode_responses = True
    )

# Bind callbacks to jwt
JWTCallbacks(jwt)

# Make app a REST api
api = Api(app, prefix=config.API_PREFIX)

# Connnect to database
db.bind(**config.DB_OPTIONS)
db.generate_mapping(create_tables=True)

# Add enpoints
api.add_resource(HandwashingRecordItem, '/handwashing-record/<int:record_id>', '/handwashing-record')

api.add_resource(HandwashingRecords, '/handwashing-record/all/<int:device_id>')
api.add_resource(AdminInfo, '/admin')
api.add_resource(UpdatePassword, '/admin/update-password')
api.add_resource(Login, '/login')
api.add_resource(SignUp, '/signup')
api.add_resource(Logout, '/logout')
if __name__ == "main":
    app.run()

