import sys
sys.path.append("..")
import numpy as np
import time

from dao.cosine import Cosine

num_entities = 10000
rng = np.random.default_rng(seed=19530)

c = Cosine(collection_name="test", dim=512)

entities = [
    [i for i in range(num_entities)],
    list(rng.random((num_entities, 512))),
]
c.insert(entities)

start_time = time.time()
scores, indexs = c.search(entities[1][7], limit=12)
end_time = time.time()
print(indexs)
print(f"search time:{end_time-start_time}s")