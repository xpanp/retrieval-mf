from flask import Response, request
from werkzeug.utils import secure_filename
import json
import os
from pathlib import Path
import cv2
import traceback
import threading
from typing import List
import time

from app.validators.forms import ADDPicForm, ADDDirForm
from app.utils.error_type import ServerError, ParameterException
from app.utils import task
from utils.config import cfg
from utils.file_client import upload
from utils.pic_trans import get_img_files
from manage.engine_manage import engine_m
from manage.db_manage import db_m
from core import algo_list
from core.utils import reduce


def get_thumbnail_name(filepath: str) -> str:
    '''
        根据原名获得缩略图名
        tmp/1.jpg -> tmp/1_th.jpg
    '''
    f = Path(filepath)
    filepath_thumbnail = f.parent.joinpath(f.stem + '_th' + f.suffix)
    return str(filepath_thumbnail)


def _add_pic(filepath: Path):
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
    if not image_thumbnail is None:
        print("use thumbnail image")
        filepath_th = get_thumbnail_name(str(filepath))
        cv2.imwrite(filepath_th, image_thumbnail)
        try:
            file_th_url = upload(cfg.FILE_SERVER_URL, filepath_th, cfg.DB_NAME)
        finally:
            # 删除临时缩略图
            os.remove(filepath_th)
    else:
        print("use raw image")
        # 若不需要缩放则使用原图url
        file_th_url = file_url

    # 遍历算法，获取每一种算法提取到的特征
    vectors = []
    for algo in algo_list:
        t1 = time.time()
        vector = engine_m.process(algo, image).tolist()
        t2 = time.time()
        print(f"algo:{algo.value} process time: {t2-t1}s")
        vectors.append(vector)

    # 插入数据库
    db_m.insert(filename=filepath.name, filepath=file_url,
                filepath_thumbnail=file_th_url, vectors=vectors)


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


class DirProcess(threading.Thread):
    '''
        后台处理线程，将文件列表中的文件依次插入到系统中，
        同时提供接口可以查看处理状态
    '''
    def __init__(self, img_files: List[Path]):
        super().__init__()
        self.img_files = img_files
        self.total_num = len(img_files)
        self.process_num = 0
        self.taskid = task.generate_task_id()

    def get_taskid(self) -> str:
        return self.taskid

    def get_total_num(self) -> int:
        return self.total_num

    def get_process_num(self) -> int:
        return self.process_num

    def progress_str(self) -> str:
        return f"taskid:{self.taskid} ------ {self.process_num} / {self.total_num}"

    def run(self):
        for i, file in enumerate(self.img_files):
            try:
                self.process_num = i
                print(self.progress_str(), "start")
                t1 = time.time()
                _add_pic(file)
                t2 = time.time()
                print(self.progress_str(), f"end, process time: {t2-t1}s")
            except Exception as e:
                print(self.progress_str() +
                      f"\nException:{e}\n{traceback.format_exc()}")
        task.delete(self.taskid)
        print(f"taskid:{self.taskid} finished!")


def add_dir():
    '''
        从文件夹批量添加图片，需提前将图片放在服务器可以访问到的文件夹下，后台处理。
        TODO: 数据库的插入应该是批量操作，可以比如每1000张图片提交一次。
        TODO: 由于是批量处理，应该申请一个handle以后一直持有，直到处理完成。
    '''
    form = ADDDirForm(request.form)
    form.validate()
    dir = Path(form.dir.data)

    img_files = get_img_files(dir)
    if len(img_files) == 0:
        raise ParameterException(
            msg=f"Can't find picture file in {dir} on target server.")
    
    dp = DirProcess(img_files)
    task.add(dp.get_taskid(), dp)
    dp.start()

    return Response(json.dumps({
        "msg": "add_dir start process",
        "taskid": dp.get_taskid(),
        "task_nums": dp.get_total_num()
    }), status=200, mimetype='application/json')
