from functools import wraps
from flask import current_app

def catch_api_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            current_app.logger.exception("Exception")
            return handle_exception(e)
    return wrapper


def handle_exception(e):
    return (
        {
            'errors': {'Error': 'Internal Server Error'},
            'message': repr(e)
        }, 500
    )


