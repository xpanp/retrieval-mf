from functools import wraps
from flask import request
from jwt import ExpiredSignatureError, InvalidSignatureError
import traceback

from utils.jwt import verify_token as vt
from app.utils.error_type import AuthError, Forbidden
from app.utils.scope import is_in_scope

def verify_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            token = request.headers["Authorization"]
            info = vt(token)
            print(info)
        except InvalidSignatureError:
            raise AuthError(msg='token is invalid')
        except ExpiredSignatureError:
            raise AuthError(msg='token is expired')
        except Exception as e:
            print(f"ip:{request.remote_addr} Exception:{e}\n{traceback.format_exc()}")
            raise AuthError(str(e))
        
        allow = is_in_scope(info['scope'], request.endpoint)
        if not allow:
            raise Forbidden()

        return func(*args, **kwargs)

    return decorator