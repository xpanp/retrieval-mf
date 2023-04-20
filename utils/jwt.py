import jwt as pyjwt
import time
from typing import Dict, Any

max_time = 60 * 60 * 24
salt = "phs820"
headers = {
  'alg': 'HS256',
  "typ": "JWT"
}

def verify_token(token:str) -> Dict[str, Any]:
    info = pyjwt.decode(jwt=token, key=salt, algorithms='HS256')
    return info

def creat_token(uid:str, scope:str):
    now = int(time.time())
    payload = {'uid': uid, 'scope': scope, 'time': now, 'exp': now + max_time}
    token = pyjwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)
    return token