from enum import Enum
from typing import List

from dao.orm_mysql import MySQL
from dao.cosine import Cosine
from dao.milvus import Milvus, connect
from utils.config import RMFConfig, cfg
from core import AlgoType, algo_list, get_dim
from utils.file_client import get_download_url


class CMPTYPE(Enum):
    MILVUS = "milvus"
    COSINE = "cosine"


class DBManager:
    '''
        数据管理，统一管理mysql数据库与向量比对数据库
        对外提供统一的insert、search、delete接口
    '''

    def __init__(self) -> None:
        self.mysql = MySQL()
        self.cmp_map = {}

    def init(self, cfg: RMFConfig):
        self.mysql.init(cfg.DSN)

        if cfg.CMP_MODE == CMPTYPE.MILVUS.value:
            # 与milvus数据库建连
            connect(cfg.MILVUS_HOST, cfg.MILVUS_PORT)
            print("milvus: start init and load vector to memory")
            self.milvus_init(cfg.DB_NAME)
            print("milvus: init success")
        elif cfg.CMP_MODE == CMPTYPE.COSINE.value:
            print("cosine: start init")
            self.cosine_init(cfg.DB_NAME)
            # 将数据库中数据加载到内存中
            self.cosine_load()
            print("cosine: init success")
        else:
            raise TypeError(f"Unsupport compare mode: {cfg.CMP_MODE}")

    def milvus_init(self, db_name: str):
        '''
            collection_name = db_name + "_" + algo_name
        '''
        for algo in algo_list:
            self.cmp_map[algo] = Milvus(db_name + "_" + algo.value, get_dim(algo))

    def cosine_init(self, db_name: str):
        for algo in algo_list:
            self.cmp_map[algo] = Cosine(db_name + "_" + algo.value, get_dim(algo))

    def cosine_load(self):
        '''
            从数据库中查询出所有数据，然后将数据加载到内存中
        '''
        print("cosine: select data from mysql")
        result = self.mysql.select_all()
        print("cosine: select success")
        print("cosine: start load vector to memory")
        for i, algo in enumerate(algo_list):
            self.cmp_map[algo].insert([result[-1], result[i]])
        print("cosine: load success")

    def insert(self, filename: str, filepath: str, filepath_thumbnail: str, vectors: List[List[float]]):
        # 插入mysql
        id = self.mysql.insert(
            filename, filepath, filepath_thumbnail, 
            vectors[0], vectors[1], vectors[2], vectors[3], vectors[4])
        # 将数据加入向量数据库
        for i, algo in enumerate(algo_list):
            self.cmp_map[algo].insert([[id], [vectors[i]]])

    def search(self, algo: AlgoType, vector: List[float], limit: int = 12) -> List[dict]:
        '''
            不同的向量对比方法得出的score是不一样的，
            milvus中使用L2距离法，因此0为距离最近，最相似
            cosine中使用余弦相似度，取值范围为[-1, 1], 1为最相似
        '''
        # 从向量数据库中找到符合条件的数据id
        scores, indexs = self.cmp_map[algo].search(vector, limit)
        # 根据id查询图片信息并返回
        result = []
        for i, id in enumerate(indexs):
            res = self.mysql.select_one(id)
            result.append({
                "id": id,
                "score": float(scores[i]),
                "filename": res[0],
                "filepath": get_download_url(cfg.FILE_SERVER_URL, res[1]),
                "filepath_thumbnail": get_download_url(cfg.FILE_SERVER_URL, res[2]),
            })
        return result


db_m = DBManager()
