import time

'''
    关于线程安全问题：
    多线程同时操作map时，由于python存在全局的锁，数据结构本身是线程安全的，不会引起崩溃。
    关于数据是否是线程安全的，由于生成的一个task是唯一的，
    工作线程结束以后也只会删除该task，因此也是线程安全的。
    详情见: https://docs.python.org/3.9/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe
'''
task = {}


def generate_task_id() -> str:
    """生成唯一的任务ID"""
    timestamp = int(time.time() * 1000)  # 获取当前时间戳（毫秒级别）
    task_id = f"task-{timestamp}"       # 生成任务ID
    return task_id


def add(key: str, value):
    task[key] = value


def get(key: str):
    return task[key]


def delete(key: str):
    del task[key]
