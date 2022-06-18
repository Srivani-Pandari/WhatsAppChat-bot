from flask import jsonify

class APIException(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        rv['message'] = self.message
        return rv