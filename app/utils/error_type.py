from flask import request
from werkzeug.exceptions import HTTPException
import json

'''
    异常处理
    flask内部异常通过继承HTTPException类来处理，
    因此我们的异常处理类继承自HTTPException来改写

    code 为http状态码
    error_code 为自定义的状态号，在http body中返回
'''

class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake!'
    error_code = 999

    def __init__(self, msg=None, code=None, headers=None):
        super().__init__()
        if code:
            self.code = code
        if msg:
            self.msg = msg

    def get_body(self, environ=None, scope=None):
        body = dict(
            code=self.error_code,
            msg=self.msg,
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope = None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0

class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1

class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake!'
    error_code = 2

class RegisterError(APIException):
    code = 500
    msg = 'register failed'
    error_code = 3

class LoginError(APIException):
    code = 401
    msg = 'login failed'
    error_code = 4

class AuthError(APIException):
    code = 401
    msg = 'authorization failed'
    error_code = 5

class Forbidden(APIException):
    code = 403
    error_code = 6
    msg = 'forbidden, not in scope'