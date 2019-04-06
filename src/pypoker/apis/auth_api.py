from flask import Flask, Blueprint, current_app, jsonify
from flask_restplus import Resource, fields, Namespace


api = Namespace('auth', description='Authentication related operations')
a_user = api.model(
    'a_user', {
        'Username': fields.String(
            required=True, 
            description= "The user's username (must be unique)"
        ),
        'Password': fields.String(
            required=True,
            description= "The user's password"
        ),
        'Email': fields.String(
            required=True,
            description="The user's email address (must be unique)"
        ),
        'Nickname': fields.String(
            description="The user's display name"
        ),
        'Bankroll': fields.Integer(
            description=(
                "The amount of currency in the user's pypoker account"
            )
)})


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
})

from ..models.user import User
from .decorators import token_required
from .validation.user_validation import (
    validate_new_user, validate_user_login)
from .decorators import token_required

@api.route("/register")
class register(Resource):
    @api.expect(a_user)
    def post(self):
        data = api.payload
        response = validate_new_user(data)
        return response.get_response()


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
        response = jsonify(token=str(user.generate_auth_token()))
        response.status_code = 200
        return response