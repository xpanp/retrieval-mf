from flask import Response, request
from werkzeug.utils import secure_filename
import json
import os
from pathlib import Path
import cv2
import traceback

from app.validators.forms import ADDPicForm
from app.utils.error_type import ServerError
from utils.config import cfg
from utils.file_client import upload
from utils.pic_trans import reduce
from manage.engine_manage import engine_m
from manage.db_manage import db_m
from core import algo_list

def get_thumbnail_name(filepath:str) -> str:
    '''
        根据原名获得缩略图名
        tmp/1.jpg -> tmp/1_th.jpg
    '''
    f = Path(filepath)
    filepath_thumbnail = f.parent.joinpath(f.stem + '_th' + f.suffix)
    return str(filepath_thumbnail)

def _add_pic(filepath:Path):
    '''
        给定一个本地图片路径，将其上传到文件服务器
        同时提取出缩略图，将缩略图也上传到文件服务器
        将所有元信息加入数据库中
    '''
    image = cv2.imread(str(filepath))

    # 上传原图，获取下载url
    file_url = upload(cfg.FILE_SERVER_URL, str(filepath), cfg.DB_NAME)

    # 获取缩略图，若返回None，则无需缩小
    image_thumbnail = reduce(src=image, dst_size=cfg.ALGO_RESIZE)
    if image_thumbnail != None:
        filepath_th = get_thumbnail_name(str(filepath))
        cv2.imwrite(filepath_th, image_thumbnail)
        try:
            file_th_url = upload(cfg.FILE_SERVER_URL, filepath_th, cfg.DB_NAME)
        finally:
            # 删除临时缩略图
            os.remove(filepath_th)
    else:
        # 若不需要缩放则使用原图url
        file_th_url = file_url

    # 遍历算法，获取每一种算法提取到的特征
    vectors = []
    for algo in algo_list:
        vector = engine_m.process(algo, image).tolist()
        vectors.append(vector)
    
    # 插入数据库
    db_m.insert(filename=filepath.name, filepath=file_url, filepath_thumbnail=file_th_url, vectors=vectors)

def add_pic():
    '''
        添加一张图片至检索系统中
    '''
    form = ADDPicForm(request.files)
    form.validate()
    file = form.file.data
    
    filepath = Path(cfg.TMP_DIR).joinpath(secure_filename(file.filename))
    file.save(filepath)

    try:
        _add_pic(filepath)
    except Exception as e:
        print(f"ip:{request.remote_addr} Exception:{e}\n{traceback.format_exc()}")
        raise ServerError(msg=str(e))
    finally:
        # 删除临时文件
        os.remove(filepath)

    return Response(json.dumps({"msg": "add_pic success"}), status=200, mimetype='application/json')


def add_dir():
    '''
        文件夹批量添加，需提前将图片放在服务器可以访问到的文件下，后台处理。
    '''
    return Response(json.dumps({"msg": "add_dir"}), status=200, mimetype='application/json')