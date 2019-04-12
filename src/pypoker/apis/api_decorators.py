from functools import wraps
from flask import request
from pypoker.models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'data': 'Token is missing'}, 401
        if not User.verify_auth_token(token):
            return {'data': 'Invalid or expired authentication token'}, 401
        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    return decorated