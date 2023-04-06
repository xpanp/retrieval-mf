import sys
sys.path.append("..")
import random
from sqlalchemy_utils import database_exists, drop_database

from dao.mysql import db
from dao.feature import DATA_VECTOR


def random_list(len:int) -> list:
    return [random.uniform(0.0, 1.0) for _ in range(len)]

dsn = "mysql+pymysql://root:LWsVjzKIO0FTdA==@127.0.0.1:3306/rmf_test1?charset=utf8mb4"
if database_exists(dsn):
    drop_database(dsn)

db.init(dsn)
DATA_VECTOR.check_and_create_table()

id = DATA_VECTOR.insert(filename="test.jpg", filepath="http://127.0.0.1/test.jpg", filepath_thumbnail="http://127.0.0.1/test_small.jpg",
          color=random_list(4), glcm=random_list(4), lbp=random_list(0), vgg=random_list(4), vit=random_list(4))
print("------------------------------")
print("insert id:", id)
print("------------------------------")

res = DATA_VECTOR.select_one(1)
print("------------------------------")
print(res)
print("------------------------------")

res = DATA_VECTOR.select_all()
print("------------------------------")
print(res)
print("------------------------------")

if database_exists(dsn):
    drop_database(dsn)