from enum import Enum


class ClientTypeEnum(Enum):
    '''
        客户端类型，目前仅支持email登录
    '''
    USER_EMAIL = 100