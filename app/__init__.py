from flask import Flask, render_template, request, redirect, url_for, session
from .database import init_database

app = Flask(__name__)
init_database()

if __name__ == "main":
    app.run()

@app.route('/api/login', methods=['POST'])
def get_token():
    return 'token'
