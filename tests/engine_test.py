import sys
sys.path.append('../')
import threading
import time

from utils.engine import EngineLock


'''
    test EngineLock in mutli threading
'''

class Algo:
    def __init__(self) -> None:
        pass

    def __call__(self, data):
        print('in process', data)
        time.sleep(0.1)
        return data


class TestEngineLock(threading.Thread):
    def __init__(self, id, engine) -> None:
        threading.Thread.__init__(self)
        self.id = id
        self.engine = engine

    def run(self): 
        try:
            res = self.engine(self.id)
            print("res: ", res)
        except Exception as e:
            print(self.id, e)
        

engines = []
for i in range(3):
    algo = Algo()
    engines.append(algo)
el = EngineLock(engines)

threads = []
for i in range(10):
    t = TestEngineLock(i, el)
    t.start()
    threads.append(t)
    time.sleep(0.03)

for t in threads:
    t.join()

