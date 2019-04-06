class ValidResponse(object):
    def __init__(self, data, code):
        self.data = data
        self.code = code

    def get_response(self):
        return {'data': self.data}, self.code, (
               {'Access-Control-Allow-Origin': '*'})


class OKResponse(ValidResponse):
    def __init__(self, data):
        ValidResponse.__init__(data, 200)


class CreatedResponse(ValidResponse):
    def __init__(self, data):
        ValidResponse.__init__(data, 201)