from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Api
from flask_cors import CORS
from app.api.resources.handwashing import HandwashingRecordItem, HandwashingRecords
from app.api.resources.device import Device, Devices
from app.api.resources.admin import AdminInfo
from app.api.resources.auth import Login, SignUp, Logout, UpdatePassword
from app.api.resources.auth import add_automatic_token_refresh
from flask_jwt_extended import JWTManager

from app.database.models import db
from app.config import config

from app.utils.callbacks import JWTCallbacks
from app.cache import CacheServices

from app.swagger_init import bind_swagger
from flask_socketio import SocketIO, emit

from app.websocket.handy_socket import PiHandyChannel

# Create flask app
app = Flask(__name__)

app.config.from_object(config)

# Add CORS Support
CORS(app)

# Add swagger Support
bind_swagger(app)

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

# Add automatic token refresh to app
add_automatic_token_refresh(app)

# Make app a REST api
api = Api(app, prefix=config.API_PREFIX)

# Connnect to database
db.bind(**config.DB_OPTIONS)
db.generate_mapping(create_tables=True)

# Add enpoints
api.add_resource(HandwashingRecordItem, '/handwashing-record/<int:record_id>', '/handwashing-record')
api.add_resource(HandwashingRecords, '/handwashing-record/all')
api.add_resource(Device, '/device')
api.add_resource(Devices, '/device/all')
api.add_resource(AdminInfo, '/admin')
api.add_resource(UpdatePassword, '/admin/update-password')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


# Create SocketIO
socketio = SocketIO(app, cors_allowed_origins='*', logger=True)
socketio.on_namespace(PiHandyChannel('/pi-frames'))

if __name__ == "main":
    socketio.run(app)

