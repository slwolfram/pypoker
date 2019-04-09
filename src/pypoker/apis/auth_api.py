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
        'Password': fields.String(
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
from .response.error_response import (
    BadRequestResponse, UnauthorizedResponse, Error)
from .response.valid_response import OKResponse

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
            r = BadRequestResponse([Error(
                source='user.Password', 
                title='Missing Required Attribute', 
                detail='Password is required to log in'
            )])
            return r.get_response()
        password = data['Password']        
        if 'Username' in data:
            user = User.fetch(username=data['Username'])
        elif 'Email' in data:
            user = User.fetch(email=data['Email'])
        if user is None:
            r = UnauthorizedResponse([Error(
                title='Invalid Attribute', 
                detail='Invalid username or email'
            )])
            return r.get_response()
        if not user.verify_password(password):
            r = UnauthorizedResponse([Error(
                source='user.Password',
                title='Access Denied', 
                detail='Invalid password'
            )])
            return r.get_response()
        r = OKResponse(data=user.generate_auth_token())
        return r.get_response()