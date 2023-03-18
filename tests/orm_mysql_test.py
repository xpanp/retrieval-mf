import sys
sys.path.append("..")
import random

from dao.orm_mysql import DB


def random_list(len:int) -> list:
    return [random.uniform(0.0, 1.0) for _ in range(len)]

db = DB()
db.init("mysql+pymysql://root:LWsVjzKIO0FTdA==@127.0.0.1:3306/rmf-test1?charset=utf8mb4")

db.insert(filename="test.jpg", filepath="http://127.0.0.1/test.jpg", filepath_samll="http://127.0.0.1/test_small.jpg",
          color=random_list(4), glcm=random_list(4), lbp=random_list(0), vgg=random_list(4), vit=random_list(4))

res = db.select_one(1)
print("------------------------------")
print(res)
print("------------------------------")

res = db.select_all()
print("------------------------------")
print(res)
print("------------------------------")