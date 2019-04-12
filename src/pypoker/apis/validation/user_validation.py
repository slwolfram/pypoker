from datetime import datetime
from flask import jsonify
from pypoker import db
from pypoker.models.user import User
from pypoker.apis.response.error_response import (
    Error, BadRequestResponse, InternalServerErrorResponse, 
    UnauthorizedResponse)
from pypoker.apis.response.valid_response import OKResponse


def validate_new_user(data):
    errors = []
    username = ""
    password = ""
    email = ""
    nickname = ""
    bankroll = 0
    # Username
    if 'Username' not in data:
        errors.append(Error(
            source="user.Username",
            title="Missing Required Attribute",
            detail="Attribute 'Username' is required"
        ))
    elif User.fetch(username=data['Username']):
        errors.append(Error(
            source="user.Username",
            title="Invalid Attribute",
            detail="Username already exists"
        ))
    elif '@' in data['Username']:
        errors.append(Error(
            source="user.Username",
            title="Invalid Attribute",
            detail="Username cannot contain '@'"
        ))
    else:
        username = data['Username']
    # Password
    if 'Password' not in data:
        errors.append(Error(
            source="user.Password",
            title="Missing Required Attribute",
            detail="Attribute 'Password' is required"
        ))
    else:
        password = data['Password']
    # Email
    if 'Email' not in data:
        errors.append(Error(
            source="user.Email",
            title="Missing Required Attribute",
            detail="Attribute 'Email' is required"
        ))
    elif User.fetch(email=data['Email']):
        errors.append(Error(
            source="user.Email",
            title="Invalid Attribute",
            detail="Email already exists"
        ))
    elif '@' not in data['Email']:
        errors.append(Error(
            source="user.Email",
            title="Invalid Attribute",
            detail="Invalid email address"
        ))
    else:
        email = data['Email']
    # Nickname
    if 'Nickname' in data:
        nickname = data['Nickname']
    
    if len(errors) != 0:
        return BadRequestResponse(errors)
    user = User(username=username, password_hash="", email=email,
                nickname=nickname, bankroll=bankroll)
    user.hash_password(password)
    if not user.create():
        return InternalServerErrorResponse([Error(
            title="Internal Server Error",
            detail="Unable to create user"
        )])
    return OKResponse(user.as_dict())


def validate_user_login(data):
    user = None
    username = ""
    password = ""
    errors = []
    if 'Password' not in data:
        errors.append(Error(
            code=400,
            source="user.Password",
            title="Missing Required Attribute",
            detail="Attribute 'Password' is Required"
        ))
    elif not user.verify_password(data['Password']):
        errors.append(Error(
            code=401,
            source="user.Password",
            title="Invalid Attribute",
            detail="Invalid Password"
        ))
    else:
        password = data['Password']        
    if 'Username' in data:
        user = User.fetch(username=data['Username'])
    elif 'Email' in data:
        user = User.fetch(email=data['Email'])
    if user is None:
        errors.append(Error(
            code=400,
            source="user.Username or user.Email",
            title="Invalid Attribute",
            detail="Invalid Username or Email"
        ))
    elif user == -1:
        return InternalServerErrorResponse([Error(
            source="user.Username or user.Email",
            title="Internal Server error"
        )])
    if len(errors) != 0:
        return BadRequestResponse(errors)
    token=str(user.generate_auth_token())
    return OKResponse(token)