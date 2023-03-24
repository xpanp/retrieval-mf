from flask import Response, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import json
import os
import time
import traceback

from app.validators.forms import SearchForm
from app.utils.error_type import ServerError
from manage.engine_manage import engine_m
from manage.db_manage import db_m
from utils.config import cfg

def search():
    # 参数验证
    form = SearchForm(CombinedMultiDict([request.form, request.files]))
    form.validate()
    file = form.file.data

    # 保存文件
    filepath = os.path.join(cfg.TMP_DIR, secure_filename(file.filename))
    file.save(filepath)

    try:
        t1 = time.time()
        # 特征提取
        vector = engine_m.process(form.algo, filepath)
        t2 = time.time()
        # 特征检索
        result = db_m.search(algo=form.algo, vector=vector.tolist(), limit=form.result_num.data)
        t3 = time.time()
        print(f'特征提取:{t2-t1}s 特征检索:{t3-t2}s')
    except Exception as e:
        print(f"ip:{request.remote_addr} Exception:{e}\n{traceback.format_exc()}")
        raise ServerError(msg=str(e))
    finally:
        # 删除临时文件
        os.remove(filepath)
 
    print(result)
    return Response(json.dumps({"msg": "ok", "compare_mode": cfg.CMP_MODE,"result": result}), status=200, mimetype='application/json')