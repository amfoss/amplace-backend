from flask import Flask, jsonify, redirect, request
from flask import session as flask_session
from flask import url_for
from flask_cors import CORS

from config import config

app = Flask(__name__)
app.secret_key = config["APP_SECRET_KEY"]



@app.route("/api/update_pixel")
def update_pixel():
    pass

@app.route("/api/get_pixel")
def get_pixel_details():
    pass 

