from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Api
from app.api.resources.handwashing import HandwashingRecordItem, HandwashingRecords
from app.api.resources.admin import AdminInfo
from app.api.resources.auth import Login
from flask_jwt_extended import JWTManager

from app.database.models import db
from app.config import config

# Create flask app
app = Flask(__name__)

app.config.from_object(config)

# Add auth service
jwt = JWTManager(app)

# Make app a REST api
api = Api(app, prefix=config.API_PREFIX)

# Connnect to database
db.bind(**config.DB_OPTIONS)
db.generate_mapping(create_tables=True)

# Add enpoints
api.add_resource(HandwashingRecordItem, '/handwashing-record/<int:record_id>', '/handwashing-record')

api.add_resource(HandwashingRecords, '/handwashing-record/all/<int:device_id>')
api.add_resource(AdminInfo, '/admin/<int:admin_id>', '/admin')
api.add_resource(Login, '/login')
if __name__ == "main":
    app.run()

