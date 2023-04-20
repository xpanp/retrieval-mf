from flask import Response, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import json
import os
import traceback
import cv2

from app.validators.forms import SearchForm, FeedbackForm
from app.utils.error_type import Success, ServerError
from manage.fusion import fusion, single_algo_process
from utils.config import cfg
from app.utils.jwt_verify import verify_token
from app.utils import task
from core import AlgoType


def check_and_intercept(filepath:str, x_min, y_min, x_max, y_max) -> bool:
    '''
        若定义的矩形框位置合法，则裁剪原图并保存到原来的图片位置
    '''
    if x_min is None or x_max is None or y_min is None or y_max is None:
        return False
    
    if x_min < 0 or x_min > x_max or y_min < 0 or y_min > y_max:
        return False
    
    img = cv2.imread(filepath)
    height = img.shape[0]
    width = img.shape[1]
    if x_max >= width or y_max >= height:
        return False
    
    img = img[y_min:y_max, x_min:x_max]
    cv2.imwrite(filepath, img)
    return True

@verify_token
def search():
    # 参数验证
    form = SearchForm(CombinedMultiDict([request.form, request.files]))
    form.validate()
    file = form.file.data

    # 保存文件
    filepath = os.path.join(cfg.TMP_DIR, secure_filename(file.filename))
    file.save(filepath)
    # 根据矩形框裁剪图片
    msg = "ok"
    if not check_and_intercept(filepath, form.x_min.data, form.y_min.data, form.x_max.data, form.y_max.data):
        msg = "uncut pictures"

    try:
        taskid = task.generate_task_id()
        if form.algo != AlgoType.FUSION:
            '''
                非融合算法则直接根据指定算法进行处理
            '''
            result = single_algo_process(form.algo, filepath, form.result_num.data)
        else:
            '''
                融合算法
            '''
            result = fusion.process(taskid=taskid, data=filepath, limit=form.result_num.data)
    except Exception as e:
        print(f"ip:{request.remote_addr} Exception:{e}\n{traceback.format_exc()}")
        raise ServerError(msg=str(e))
    finally:
        # 删除临时文件
        os.remove(filepath)
 
    print(result)
    return Response(json.dumps({"code": 0, 
                                "msg": msg, 
                                "data":{
                                    "taskid": taskid,
                                    "compare_mode": cfg.CMP_MODE, 
                                    "result": result
                                    }
                                }), 
                    status=200, mimetype='application/json')


@verify_token
def feedback():
    # 参数验证
    form = FeedbackForm(request.form)
    form.validate()

    try:
        fusion.feedback(taskid=form.taskid.data, pictureid=form.pictureid.data, type=form.type.data)
    except Exception as e:
        # 即使有错误也不用返回，对用户来说是无感的
        print(f"ip:{request.remote_addr} Exception:{e}\n{traceback.format_exc()}")

    return Success()