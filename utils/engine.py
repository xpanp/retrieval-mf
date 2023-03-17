import threading


class EngineLock:
    '''
        引擎管理模块，传入初始化好的多个引擎模块。
        每次需要处理时调用process()函数并传入待处理数据。
        若存在可用handle则进行处理，若不存在可用handle则抛出异常。
    '''
    def __init__(self, engines:list) -> None:
        self.max_worker_num = len(engines)
        self.worker_num = len(engines)
        self.engines = engines
        self.engines_flag = [True] * len(engines)
        self.lock = threading.Lock()
    
    # 获取可用的handle id，-1为无可用的handle
    def get_handle(self) -> int:
        handle = -1
        self.lock.acquire()
        if self.worker_num > 0:
            self.worker_num -= 1
            for index, flag in enumerate(self.engines_flag):
                if flag == True:
                    handle = index
                    self.engines_flag[index] = False
                    break
            assert(handle != -1)
        self.lock.release()
        return handle

    # 释放handle, 加入可用资源池
    def free_handle(self, handle:int):
        self.lock.acquire()
        if handle != -1:
            self.worker_num += 1
            self.engines_flag[handle] = True
        self.lock.release()

    # 返回单张图片识别结果, 不加锁
    def _process(self, handle:int, data):
        try:
            if handle < 0:
                raise ValueError("Can't get handle!")
            res = self.engines[handle](data)
        except Exception as e:
            raise e
        return res

    def process(self, data):
        handle = self.get_handle()
        try:
            res = self._process(handle, data)
        except Exception as e:
            raise e
        finally:
            self.free_handle(handle)
        return res
    
    def __call__(self, data):
        return self.process(data)