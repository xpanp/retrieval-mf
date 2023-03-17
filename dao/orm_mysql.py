import datetime
import struct
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    LargeBinary,
    DateTime,
    Boolean,
    inspect,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

# 基础类
Base = declarative_base()

class DB():
    def __init__(self, url) -> None:
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

        # 判断表是否存在，不存在则创建
        if not inspect(self.engine).has_table(DATA_VECTOR.__tablename__):
            # Base.metadata.drop_all(db.engine) # 删除表
            Base.metadata.create_all(self.engine) # 创建表

        # 绑定引擎
        self.Session = sessionmaker(bind=self.engine)
        # 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
        # 内部会采用threading.local进行隔离
        self.session = scoped_session(self.Session)

    def insert(self, filename:str, filepath:str, filepath_samll:str, color:List[float],
               glcm:List[float], lbp:List[float], vgg:List[float], vit:List[float]):
        color = struct.pack('%sf' % len(color), *color)
        glcm = struct.pack('%sf' % len(glcm), *glcm)
        lbp = struct.pack('%sf' % len(lbp), *lbp)
        vgg = struct.pack('%sf' % len(vgg), *vgg)
        vit = struct.pack('%sf' % len(vit), *vit)
        instance = DATA_VECTOR(
            FILENAME=filename,
            FILEPATH=filepath,
            FILEPATH_SMALL=filepath_samll,
            COLORFEAT=color,
            GLCMFEAT=glcm,
            LBPFEAT=lbp,
            VGGFEAT=vgg,
            VITFEAT=vit,
        )
        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print("insert failed, ", filename, e)
            raise e
        finally:
            self.session.close()

    def select_all(self) -> List[list]:
        try:
            result = self.session.query(DATA_VECTOR.ID, DATA_VECTOR.FILENAME, DATA_VECTOR.FILEPATH, DATA_VECTOR.FILEPATH_SMALL,
                                        DATA_VECTOR.COLORFEAT, DATA_VECTOR.GLCMFEAT, DATA_VECTOR.LBPFEAT, 
                                        DATA_VECTOR.VGGFEAT, DATA_VECTOR.VITFEAT).all()
        except Exception as e:
            print("select fail", e)
        finally:
            self.session.close()
        
        ress = []
        for r in result:
            res = []
            try:
                res.append(r[0])
                res.append(r[1])
                res.append(r[2])
                res.append(r[3])
                color = list(struct.unpack('{}f'.format(int(len(r[4])/4)), r[4]))
                res.append(color)
                glcm = list(struct.unpack('{}f'.format(int(len(r[5])/4)), r[5]))
                res.append(glcm)
                lbp = list(struct.unpack('{}f'.format(int(len(r[6])/4)), r[6]))
                res.append(lbp)
                vgg = list(struct.unpack('{}f'.format(int(len(r[7])/4)), r[7]))
                res.append(vgg)
                vit = list(struct.unpack('{}f'.format(int(len(r[8])/4)), r[8]))
                res.append(vit)
            except Exception as e:
                print("struct.unpack error:", e)
            ress.append(res)
        return ress

    def select_one(self, id:int) -> tuple:
        try:
            result = self.session.query(
                DATA_VECTOR.FILENAME, DATA_VECTOR.FILEPATH, DATA_VECTOR.FILEPATH_SMALL
            ).filter(
                DATA_VECTOR.ID == id
            ).all()
        except Exception as e:
            print("select fail", e)
        finally:
            self.session.close()
        
        assert(len(result) == 1)
        return result[0]


class DATA_VECTOR(Base):
    """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "DATA_VECTOR"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    ID = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    FILENAME = Column(String(64), unique=True, nullable=False, comment="图片名称")
    FILEPATH = Column(String(256), nullable=False, comment="图片地址")
    FILEPATH_SMALL = Column(String(256), nullable=False, comment="缩略图地址")

    # 对于非必须插入的字段，不用采取nullable=False进行约束
    COLORFEAT = Column(LargeBinary, comment="color特征向量")
    GLCMFEAT = Column(LargeBinary, comment="glcm特征向量")
    LBPFEAT = Column(LargeBinary, comment="lbp特征向量")
    VGGFEAT = Column(LargeBinary, comment="vgg特征向量")
    VITFEAT = Column(LargeBinary, comment="vit特征向量")
    create_time = Column(
        DateTime, default=datetime.datetime.now, comment="创建时间")
    last_update_time = Column(
        DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")
    delete_status = Column(Boolean(), default=False,
                           comment="是否删除")

    # __table__args__ = (
    #     UniqueConstraint("FILENAME"),  # 联合唯一约束
    #     Index("ID", "FILENAME", unique=True),  # 联合唯一索引
    # )

    def __str__(self):
        return f"object : <ID:{self.ID} FILENAME:{self.FILENAME}>"
