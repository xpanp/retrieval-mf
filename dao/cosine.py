import torch
from typing import List

'''
    提供一个和milvus接口一致的传统检索方法，使用余弦相似性进行比对检索。
    一方面可以和milvus的结果进行对比，
    另一方面可以选择使用cosine方法简化部署。
    但需要注意，由于Cosine类仅管理内存数据，因此初始化以及向量的落盘需要
    在类外单独进行管理。需要注意数据一致性问题。
'''

def compare(k:torch.Tensor, f:torch.Tensor):
    return torch.cosine_similarity(k, f, dim=0)

class Cosine:
    def __init__(self, collection_name:str, dim:int) -> None:
        self.collection_name = collection_name
        self.dim = dim
        self.feats = []
        '''
            数据非本地管理，而每一条数据在数据库中都有一个对应的唯一ID
            检索返回的应该是该数据的唯一ID，而不是self.feats中的数组编号
            因此用self.indexs存储数据ID的映射关系
        '''
        self.indexs = []

    def insert(self, entities: List[List]):
        '''
            insert, 批量插入数据
            entities = [
                # [id, ]
                [i for i in range(num_entities)],
                # [embeddings, ] 
                [[random() for j in range(dim)] for i in range(num_entities)],    
            ]
        '''
        for i in range(len(entities[1])):
            if len(entities[1][i]) == self.dim:
                self.indexs.append(entities[0][i])
                self.feats.append(torch.Tensor(entities[1][i]))

    def search(self, vector: List[float], limit: int = 12) -> tuple[List[float], List[int]]:
        if len(vector) != self.dim:
            raise TypeError(f"vector's dim must be {self.dim}")
        results = []
        for i in range(len(self.feats)):
            score = compare(torch.Tensor(vector), self.feats[i])
            results.append((score, i))
        results.sort(key=lambda elem:elem[0], reverse=True)
        scores = []
        indexs = []
        res_num = min(limit, len(results))
        for i in range(res_num):
            scores.append(results[i][0])
            indexs.append(self.indexs[results[i][1]])
        return scores, indexs
