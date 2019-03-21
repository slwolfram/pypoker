from flask import jsonify

def bad_request(msg, code):
    response = jsonify({
        'error': msg
    })
    response.status_code = code
    return response

def good_request(msg, code):
    response = jsonify({
        'data': msg
    })
    response.status_code = code
    return response