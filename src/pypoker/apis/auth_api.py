from flask import Flask, Blueprint, current_app, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Api, Resource, fields

auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

from ..models.user import User
from .validation.user_validation import validate_user
from .validation.response import bad_request, good_request
from . import auth

a_user = api.model(
    'a_user', {
        'Username': fields.String(
            required=True, 
            description= "The user's username (must be unique)"
        ),
        'Password': fields.Integer(
            required=True,
            description= "The user's password"
        ),
        'Email': fields.Integer(
            required=True,
            description="The user's email address (must be unique)"
        ),
        'Nickname': fields.Integer(
            description="The user's display name"
        ),
        'Bankroll': fields.Integer(
            description=(
                "The amount of currency in the user's pypoker account"
            )
        )
    }
)

a_login = api.model(
    'a_login', {
        'Username': fields.String(
            description= "The user's username"
        ),
        'Password': fields.Integer(
            required=True,
            description= "The user's password"
        ),
        'Email': fields.Integer(
            description="The user's email address"
        )
    }
)

@api.route("/register")
class register(Resource):
    @api.expect(a_user)
    def post(self):
        data = api.payload
        return validate_user(data)

@api.route("/login")
class login(Resource):
    @api.expect(a_login)
    def post(self):
        data = api.payload
        user = None
        if 'Password' not in data:
            return bad_request('Password is required to login in', 400)
        password = data['Password']        
        if 'Username' in data:
            user = User.fetch(username=data['Username'])
        elif 'Email' in data:
            user = User.fetch(email=data['Email'])
        if user is None:
            return bad_request('Invalid username or email', 400)
        if not user.verify_password(password):
            return bad_request(
                'Authentication error. Bad password.', 404)
        return user.generate_auth_token()

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    return True