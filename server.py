import argparse
from flask import Flask
from flask_cors import CORS

from utils.config import cfg
from engine_manage import engineM
from dao.orm_mysql import db

app = Flask("rmf")
CORS(app, supports_credentials=True)


def retrieval():
    '''
        检索接口：
        参数处理，提取特征，在线比对，根据id在数据库中找到图片url并返回
    '''
    pass


def add_pic():
    '''
        添加图片
        参数处理，图片上传文件服务器（包括缩略图），提取特征，插入数据库，更新在线内存中数据
    '''
    pass


def add_dir():
    '''
        文件夹批量添加，需提前将图片放在服务器可以访问到的文件下，后台处理。
    '''
    pass


def get_args():
    # 获取命令行参数
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', type=str, default="conf/conf.ini",
                        help='config file')

    args = parser.parse_args()

    return args


def main():
    args = get_args()
    cfg.parser(args.c)
    # 特征提取引擎初始化
    engineM.init(cfg)

    app.run(host=cfg.HOST, port=cfg.PORT, debug=cfg.DEBUG)


if __name__ == '__main__':
    main()
