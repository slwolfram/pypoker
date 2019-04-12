from flask import Flask, Blueprint, current_app, jsonify
from flask_restplus import (
    Resource, fields, Namespace, reqparse, inputs)
from .api_decorators import token_required
from ..models.user import User
from .api_decorators import token_required
from .validation.user_validation import (
    validate_new_user, validate_user_login)
from .response.error_response import (
    BadRequestResponse, UnauthorizedResponse, Error)
from .response.valid_response import OKResponse


api = Namespace(
    'auth', description='Authentication related operations')


register_parser = api.parser()
register_parser.add_argument(
    'Username', 
    type=str, 
    required=True, location='form')
register_parser.add_argument(
    'Password', 
    type=str, 
    required=True, location='form')
register_parser.add_argument('Email', 
    type=str, 
    required=True, location='form')
register_parser.add_argument(
    'Nickname', 
    type=str, 
    location='form')

@api.route("/register")
class register(Resource):
    @api.doc(parser=register_parser)
    def post(self):
        data = register_parser.parse_args()
        response = validate_new_user(data)
        return response.get_response()


login_parser = api.parser()
login_parser.add_argument(
    'Identifier', 
    type=inputs.regex('^[a-zA-Z][a-zA-Z0-9@\.]{1,16}$'), 
    required=True, help='Username or Email', location='form')
login_parser.add_argument(
    'Password', 
    type=inputs.regex('^[A-Za-z0-9@\!\?\$\-\_\.\*\(\)]{8,24}$'),
    required=True, location='form')

@api.route("/login")
class login(Resource):
    @api.doc(parser=login_parser)
    def post(self):
        data = login_parser.parse_args()
        password = data['Password']  
        user = User.fetch(email=data['Identifier']) \
            if '@' in data['Identifier'] \
            else User.fetch(username=data['Identifier'])
        if user is None:
            r = UnauthorizedResponse([Error(
                title='Invalid Attribute', 
                detail='Invalid username or email'
            )])
            return r.get_response()
        if not user.verify_password(password):
            r = UnauthorizedResponse([Error(
                title='Access Denied', 
                detail='Invalid password'
            )])
            return r.get_response()
        r = OKResponse(data=user.generate_auth_token())
        return r.get_response()
