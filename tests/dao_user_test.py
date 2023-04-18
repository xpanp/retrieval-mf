import sys
sys.path.append("..")
import random
from sqlalchemy_utils import database_exists, drop_database

from dao.mysql import db
from dao.user import User


def random_list(len:int) -> list:
    return [random.uniform(0.0, 1.0) for _ in range(len)]

dsn = "mysql+pymysql://root:LWsVjzKIO0FTdA==@127.0.0.1:3306/rmf_test1?charset=utf8mb4"
if database_exists(dsn):
    drop_database(dsn)

db.init(dsn)
User.check_and_create_table()

def register(name:str, email:str, passwd:str):
    try:
        id = User.register_by_email(name=name, email=email, passwd=passwd)
        print('id:', id)
    except Exception as e:
        print(e)

print("1------------------------------1")
register(name='phs', email='phs95825@qq.com', passwd='123456')
print("1------------------------------1")

print("2------------------------------2")
register(name='phs2', email='12345@qq.com', passwd='areaewraf')
print("2------------------------------2")

def verify(email:str, passwd:str):
    try:
        res = User.verify(email=email, passwd=passwd)
        print(res)
    except Exception as e:
        print(e)

print("3------------------------------3")
verify(email='phs95825@qq.com', passwd='123456')
print("3------------------------------3")

print("4------------------------------4")
verify(email='phs9585@qq.com', passwd='123456')
print("4------------------------------4")

print("5------------------------------5")
verify(email='phs95825@qq.com', passwd='12345')
print("5------------------------------5")

if database_exists(dsn):
    drop_database(dsn)