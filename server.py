import argparse

from utils.config import cfg
from manage.engine_manage import engine_m
from manage.db_manage import db_m
from manage.fusion import fusion
from dao.mysql import db
from dao.feature import DATA_VECTOR
from dao.user import User
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
    # 特征融合模块初始化
    fusion.init(cfg)
    '''
        这里表的检查顺序很重要。
        检查第一张表时，若其他表不存在，也会一起创建。
        若第一张表存在，继续检查第二张表，第二张表不存在则仅创建第二张表。
        由于User表创建之初还需要插入管理员用户，因此需要先检查User表。
    '''
    User.check_and_create_table()
    DATA_VECTOR.check_and_create_table()
    db_m.init(cfg)

    # 将app封装，则系统与web框架分离
    app = create_app()
    app.set_cfg(cfg)
    app.start()


if __name__ == '__main__':
    main()
