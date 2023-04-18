from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

# 基础类
Base = declarative_base()


class MySQL():
    def __init__(self) -> None:
        pass

    def init(self, url:str):
        # 创建引擎
        self.engine = create_engine(
            url,
            # 超过链接池大小外最多创建的链接
            max_overflow=0,
            # 链接池大小
            pool_size=5,
            # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
            pool_timeout=10,
            # 多久之后对链接池中的链接进行一次回收
            pool_recycle=1,
            # 查看原生语句（未格式化）
            echo=True
        )

        # 判断数据库是否存在，不存在则创建
        if not database_exists(self.engine.url):
            create_database(self.engine.url)


    def get_session(self):
        return scoped_session(sessionmaker(bind=self.engine))


    @contextmanager
    def auto_commit(self, raise_flag=True):
        '''
            raise_flag: 是否抛出异常
        '''
        # 绑定引擎
        # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
        # 内部会采用threading.local进行隔离
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            if raise_flag:
                raise e
        finally:
            '''
                Close out the transactional resources and ORM objects used by this Session.
                Proxied for the Session class on behalf of the scoped_session class.
                若不进行关闭，可能导致如删除表这类操作卡住
                这里只是将连接释放到连接池，并不是真正关闭了该连接
            '''
            if session:
                session.close()

db = MySQL()