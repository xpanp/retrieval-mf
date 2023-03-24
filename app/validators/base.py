from wtforms import Form

from app.utils.error_type import ParameterException


class BaseForm(Form):
    '''
        参数验证基类，需要手动调用validate函数进行验证。
        若验证不通过会自动被错误异常处理所捕获，并返回。
        对于POST请求，初始化参数需传入request.form，
        对于GET请求，初始化参数需传入request.args
    '''
    def validate(self):
        valid = True
        try:
            valid = super().validate()
        except Exception as e:
            raise ParameterException(msg=str(e))
        if not valid:
            raise ParameterException(msg=str(self.errors))