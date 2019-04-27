from functools import wraps
from flask import request
from ..models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        if 'Authorization' in request.headers:
            print(request.headers)
            token = request.headers['Authorization']
            token = token.replace('Bearer ', '')
        if not token:
            return {'data': 'Token is missing'}, 401
        if not User.verify_auth_token(token):
            return {'data': 'Invalid or expired authentication token'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated