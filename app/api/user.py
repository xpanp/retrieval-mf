from flask import Response, request
import traceback
import json

from app.validators.forms import ClientForm, UserEmailForm
from app.utils.error_type import Success, RegisterError, LoginError
from dao.user import User
from utils.jwt import creat_token

def register():
    '''
        用户注册，使用email注册账户
        仅支持注册普通用户
    '''
    form = UserEmailForm(request.form)
    form.validate()

    try:
        User.register_by_email(name=form.nickname.data, 
                            email=form.account.data, passwd=form.passwd.data)
    except Exception as e:
        print(f"ip:{request.remote_addr} Exception:{e}\n{traceback.format_exc()}")
        raise RegisterError(msg=str(e))
    
    return Success()


def login():
    '''
        根据登录信息返回token
    '''
    form = ClientForm(request.form)
    form.validate()

    try:
        userinfo = User.verify(form.account.data, form.passwd.data)
        token = creat_token(uid=userinfo['uid'], scope=userinfo['scope'])
        t = {
            "token": token
        }
    except Exception as e:
        print(f"ip:{request.remote_addr} Exception:{e}\n{traceback.format_exc()}")
        raise LoginError(msg=str(e))
    return Response(json.dumps({"code": 0, "msg": "ok", "data": t}), 
                    status=200, mimetype='application/json')