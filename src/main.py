from flask import Flask, request, session
import os
from flask_cors import CORS

from src.signup import UserSignup
from src.login import UserLogin

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

@app.route("/user/signup", methods=["POST"])
def signup():
    if 'database' not in session.keys():
        session['database'] = dict()
    userSignup = UserSignup(request.get_json(), session['database']).signup()
    if userSignup[1]["status"] == "success":
        session['database'] = userSignup[0]
    return {"message": userSignup[1]["message"]}, userSignup[1]["code"]

@app.route("/user/login", methods=["POST"])
def login():
    if 'database' not in session.keys():
        session['database'] = dict()
    userLogin = UserLogin(request.get_json(), session['database']).login()
    userData = None
    if userLogin[1]["status"] == "success":
        userData = userLogin[0]
    return {"message": userLogin[1]["message"], "data": userData}, userLogin[1]["code"]