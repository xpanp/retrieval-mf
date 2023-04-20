from typing import Union, List
from cv2 import Mat
import time
from enum import Enum

from utils import config
from core import algo_list, AlgoType
from manage.db_manage import db_m
from manage.engine_manage import engine_m


def single_algo_process(algo:AlgoType, data: Union[str, Mat], limit:int) -> List[dict]:
    '''
        指定特征提取算法，检索最为相近的结果
    '''
    t1 = time.time()
    # 特征提取
    vector = engine_m.process(algo, data)
    t2 = time.time()
    # 特征检索
    result = db_m.search(algo=algo, vector=vector.tolist(), limit=limit)
    t3 = time.time()
    print(f'algo: {AlgoType.VIT.value} 特征提取:{t2-t1}s 特征检索:{t3-t2}s')
    return result


class FeedbackEnum(Enum):
    '''
        反馈搜索结果
    '''
    BAD = 0
    GOOD = 1


class Fusion:
    def __init__(self) -> None:
        pass

    def init(self, cfg:config.RMFConfig) -> None:
        '''
            初始化系数
        '''
        pass

    def process(self, taskid:str, data: Union[str, Mat], limit:int) -> List[dict]:
        '''
            TODO 特征融合待实现，目前直接使用指定算法
        '''
        result = single_algo_process(AlgoType.VIT, data, limit)
        
        return result

    def feedback(self, taskid:str, pictureid:int, type:FeedbackEnum):
        '''
            TODO 基于反馈修改权值
        '''
        pass


fusion = Fusion()