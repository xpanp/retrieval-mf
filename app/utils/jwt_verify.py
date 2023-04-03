from functools import wraps
from flask import request
from jwt import ExpiredSignatureError

from utils.jwt import verify_token as vt
from app.utils.error_type import LoginError

def verify_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            token = request.headers["token"]
            info = vt(token)
            print(info)
        except ExpiredSignatureError:
            raise LoginError()
        except Exception as e:
            raise LoginError(str(e))

        return func(*args, **kwargs)

    return decorator