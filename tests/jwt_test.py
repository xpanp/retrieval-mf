import sys
sys.path.append('../')
import time
from jwt import ExpiredSignatureError

from utils import jwt

jwt.max_time = 1

token = jwt.creat_token("12345")
print(token)

info = jwt.verify_token(token)
print(info)

time.sleep(2)
try:
    info = jwt.verify_token(token)
    print(info)
except ExpiredSignatureError as e:
    print(e)
