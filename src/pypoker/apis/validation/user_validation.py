from datetime import datetime
from flask import jsonify
from pypoker import db
from pypoker.models.user import User
from pypoker.apis.validation.response import bad_request, good_request

def validate_user(data):
    # Username
    if 'Username' not in data:
        return bad_request("Request field 'Username' is required", 400)
    if User.fetch(username=data['Username']):
        return bad_request("Username already exists", 400)
    username = data['Username']
    # Password
    if 'Password' not in data:
        return bad_request("Request field 'Password' is required", 400)  
    password = data['Password']
    # Email
    if 'Email' not in data:
        return bad_request("Request field 'Email' is required", 400)
    if User.fetch(email=data['Email']):
        return bad_request("Email already exists", 400)
    email = data['Email']
    # Nickname
    nickname = ""
    if 'Nickname' in data:
        nickname = data['Nickname']
    # Bankroll
    bankroll = 0
    if 'Bankroll' in data:
        bankroll = data['Bankroll']
    user = User(username=username, password_hash="", email=email,
                nickname=nickname, bankroll=bankroll)
    user.hash_password(password)
    if user.create():
        return good_request(user.as_dict(), 201)
    return bad_request("Couldn't create user.", 500)