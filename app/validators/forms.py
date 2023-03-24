from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileRequired, FileAllowed, FileSize

from app.validators.base import BaseForm
from core import AlgoType

'''
    request参数定义，指定字段并进行限制
'''

class SearchForm(BaseForm):
    algo = StringField(validators=[DataRequired()])
    result_num = IntegerField(validators=[DataRequired(), NumberRange(min=1, max=30)])
    file = FileField(validators=[FileRequired(), FileAllowed(['jpg','png','bmp']), FileSize(max_size=20*1024*1024)])

    def validate_algo(self, value):
        try:
            algo = AlgoType(value.data)
        except ValueError as e:
            raise e
        self.algo = algo

class ADDPicForm(BaseForm):
    # 图片不应该超过20M，同时后缀名应该正确（大小写无关）
    file = FileField(validators=[FileRequired(), FileAllowed(['jpg','png','bmp']), FileSize(max_size=20*1024*1024)])
