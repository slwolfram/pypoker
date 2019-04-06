class Error(object):
    def __init__(self, **kwargs):
        if 'source' in kwargs:
            self.source = kwargs['source']
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'detail' in kwargs:
            self.detail = kwargs['detail']
        if 'status' in kwargs:
            self.status = kwargs['status']

    def as_dict(self):
        error_dict = {}
        if hasattr(self, 'status'):
            error_dict['status'] = self.status
        if hasattr(self, 'source'):
            error_dict['source'] = self.source
        if hasattr(self, 'title'):
            error_dict['title'] = self.title
        if hasattr(self, 'detail'):
            error_dict['detail'] = self.detail
        return error_dict
        
        
class InternalServerError(Error):
    def __init__(self, **kwargs):
        if 'source' in kwargs:
            self.source = kwargs['source']
        self.title = 'Internal Server Error'
        if 'detail' in kwargs:
            self.detail = kwargs['detail']
        if 'show_status' in kwargs and kwargs['show_status']:
            self.status = 500
        

class ErrorResponse(object):
    def __init__(self, errors, code):
        self.errors = errors
        self.code = code

    def get_response(self):
        return {'errors': self.errors}, self.code, (
               {'Access-Control-Allow-Origin': '*'})


class BadRequestResponse(ErrorResponse):
    def __init__(self, errors):
        ErrorResponse.__init__(
            errors, 400
        )


class UnauthorizedResponse(ErrorResponse):
    def __init__(self, errors):
        ErrorResponse.__init__(
            errors, 401
        )

class NotFoundResponse(ErrorResponse):
    def __init__(self, errors):
        ErrorResponse.__init__(
            errors, 404
        )

class InternalServerErrorResponse(ErrorResponse):
    def __init__(self, errors):
        ErrorResponse.__init__(
            errors, 500
        )