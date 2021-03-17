from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

if __name__ == "main":
    app.run()

@app.route('/api/login', methods=['POST'])
def get_token():
    return 'token'
