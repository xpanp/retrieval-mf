import argparse

from utils.config import cfg
from manage.engine_manage import engine_m
from manage.db_manage import db_m
from dao.mysql import db
from app import create_app

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
    engine_m.init(cfg)
    # 数据库模块初始化
    db.init(cfg.DSN)
    db_m.init(cfg)

    # 将app封装，则系统与web框架分离
    app = create_app()
    app.set_cfg(cfg)
    app.start()


if __name__ == '__main__':
    main()
