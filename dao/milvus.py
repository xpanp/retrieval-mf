from typing import List
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

'''
    milvus是一个向量数据库，可以自动保存数据到磁盘，
    因此每次启动可以自动将向量数据加载到内存中
'''


def connect(host: str, port: int):
    '''
        全局唯一，必须先建立全局的连接，后续才可以操作不同的collection
    '''
    connections.connect("default", host=host, port=str(port))


def drop_collection(collection_name: str):
    '''
        删除collection
    '''
    has = utility.has_collection(collection_name)
    if has:
        utility.drop_collection(collection_name)


def generate_fields(dim: int) -> List[FieldSchema]:
    '''
        dim字段为向量长度, mysql中无需设置,
        这里需要设置为对应算法提取出的向量长度,
        具体值对应各个算法
    '''
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64,
                    is_primary=True, auto_id=False),
        FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim),
    ]
    return fields


class Milvus:
    def __init__(self, collection_name: str, dim: int) -> None:
        '''
            根据collection_name创造Milvus实例，必须正确指定向量维度dim
        '''
        self.collection_name = collection_name
        has = utility.has_collection(self.collection_name)
        print(f"Does collection {self.collection_name} exist in Milvus: {has}")
        if not has:
            # 不存在集合则创建
            fields = generate_fields(dim)
            schema = CollectionSchema(
                fields, f"{self.collection_name} is the feature of the image.")
            self.collection = Collection(
                self.collection_name, schema, consistency_level="Strong")
        else:
            # 已存在集合，直接使用
            self.collection = Collection(self.collection_name)
            print(f"Number of entities in {self.collection_name}: {self.collection.num_entities}")

        self.create_index()
        # 需要手动将数据加载到内存中
        self.collection.load()

    def release(self):
        # 从内存中卸载，减少内存使用
        self.collection.release()

    def insert(self, entities: List[List]):
        '''
            insert, 批量插入数据
            entities = [
                # [id, ]
                [i for i in range(num_entities)],
                # [embeddings, ] supports numpy.ndarray and list
                [[random() for j in range(dim)] for i in range(num_entities)],    
            ]
        '''
        self.collection.insert(entities)
        self.collection.flush()

    def search(self, vector: List[float], limit: int = 12) -> tuple[List[float], List[int]]:
        '''
            search, 使用单组向量进行检索
            vector: 待检索向量，len必须等于self.dim
            limit: 限制返回数量，返回结果不超limit

            return: scores为得分列表，indexs为相应的ID
        '''
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }

        result = self.collection.search(
            [vector], "embeddings", search_params, limit=limit, output_fields=["id"])

        scores = []
        indexs = []
        for hit in result[0]:
            scores.append(float(hit.score))
            indexs.append(hit.id)
        return scores, indexs

    def create_index(self):
        if self.collection.has_index(index_name="idx"):
            return
        print("Start Creating index IVF_FLAT")
        index = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128},
        }

        self.collection.create_index("embeddings", index, index_name="idx")
        print("Creating index IVF_FLAT success")
