from pathlib import Path
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired, NumberRange, length, Email, Regexp, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileSize

from app.validators.base import BaseForm
from core import AlgoType
from utils.pic_trans import img_extensions
from app.utils.enums import ClientTypeEnum
from manage.fusion import FeedbackEnum

'''
    request参数定义，指定字段并进行限制
'''

class SearchForm(BaseForm):
    algo = StringField(validators=[DataRequired()])
    result_num = IntegerField(validators=[DataRequired(), NumberRange(min=1, max=30)])
    x_min = IntegerField()
    y_min = IntegerField()
    x_max = IntegerField()
    y_max = IntegerField()
    file = FileField(validators=[FileRequired(), FileAllowed(img_extensions), FileSize(max_size=20*1024*1024)])

    def validate_algo(self, value):
        try:
            algo = AlgoType(value.data)
        except ValueError as e:
            raise e
        self.algo = algo

class FeedbackForm(BaseForm): 
    taskid = StringField(validators=[DataRequired()])
    pictureid = IntegerField(validators=[DataRequired()])
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            v = FeedbackEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = v


class ADDPicForm(BaseForm):
    # 图片不应该超过20M，同时后缀名应该正确（大小写无关）
    file = FileField(validators=[FileRequired(), FileAllowed(img_extensions), FileSize(max_size=20*1024*1024)])

class ADDDirForm(BaseForm):
    # 文件夹路径必须是在服务器上真实存在的路径
    dir = StringField(validators=[DataRequired()])

    def validate_dir(self, dir):
        try:
            dir = Path(dir.data)
            if not dir.is_dir():
                raise IsADirectoryError(f"Can't find folder {dir} on target server")
        except Exception as e:
            raise e

class StatusForm(BaseForm):
    taskid = StringField(validators=[DataRequired()])
        

class ClientForm(BaseForm):
    '''
        登录
    '''
    account = StringField(validators=[DataRequired(message='account is required'), length(min=5, max=32)])
    passwd = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client

class UserEmailForm(ClientForm):
    '''
        使用email进行注册
    '''
    account = StringField(validators=[DataRequired(), Email(message='invalidate email')])
    passwd = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(), length(min=2, max=22)])