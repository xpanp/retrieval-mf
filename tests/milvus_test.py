import sys
sys.path.append("..")
import numpy as np
import time

from dao.milvus import Milvus, connect, drop_collection

collection_name = "milvus_test"
num_entities = 10000
rng = np.random.default_rng(seed=19530)

connect(host="localhost", port=19530)
drop_collection(collection_name)

milvus = Milvus(collection_name=collection_name, dim=512)

entities = [
    [i for i in range(num_entities)],
    rng.random((num_entities, 512)),    # field embeddings, supports numpy.ndarray and list
]
milvus.insert(entities)

start_time = time.time()
scores, indexs = milvus.search(entities[1][7], limit=12)
end_time = time.time()
print(indexs)
print(f"search time:{end_time-start_time}s")

drop_collection(collection_name)