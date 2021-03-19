from flask import Flask, render_template, request, redirect, url_for, session
from app.database import init_database
from flask_restful import Api
from app.api.resources.handwashing import HandwashingRecordItem

# Create flask app
app = Flask(__name__)

# Make app a REST api
api = Api(app, prefix='/v1')

# Connnect to database
init_database()

# Add enpoints
api.add_resource(HandwashingRecordItem, '/handwashing-record/<int:record_id>', '/handwashing-record')

if __name__ == "main":
    app.run()

