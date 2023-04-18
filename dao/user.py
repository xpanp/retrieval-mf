from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import (
    inspect,
    Column,
    Integer,
    String,
    SmallInteger,
)
from dao.mysql import db, Base

UserScope = 1
AdminScope = 2

class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    email = Column(String(24), unique=True, nullable=False, comment="邮箱")
    nickname = Column(String(24), unique=True, comment="人名")
    auth = Column(SmallInteger, default=UserScope, comment="权限")
    _password = Column('password', String(108), comment="密码")

    def __str__(self):
        return f"object : <id:{self.id} name:{self.nickname} email:{self.email}>"
    
    @staticmethod
    def check_and_create_table():
        # 判断表是否存在，不存在则创建
        if not inspect(db.engine).has_table(User.__tablename__):
            # Base.metadata.drop_all(db.engine) # 删除表
            Base.metadata.create_all(db.engine) # 创建表
    
    @property
    def password(self):
        '''
            @property装饰器会将方法转换为相同名称的只读属性
        '''
        return self._password
    
    @password.setter
    def password(self, raw):
        '''
            python中的@*.setter装饰器可以总结为两个作用：
            1. 对要存入的数据进行预处理
            2. 设置可读属性(不可修改)
            注意：@*.setter装饰器必须在@property装饰器的后面，且两个被修饰的函数的名称必须保持一致，* 即为函数名称。

            生成密码样例，长度为102个字符
            pbkdf2:sha256:260000$UzuWfq42Idn0sFcF$1eb9ae0aec573f24c3687d860de1d3e0c0b1378249480c0ea4fe1f9718b04c95
        '''
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(name:str, email:str, passwd:str) -> int:
        user = User()
        user.nickname = name
        user.email = email
        user.password = passwd

        session = db.get_session()
        try:
            session.add(user)
            session.commit()
            # commit成功以后才可以得到对应的id
            id = user.id
        except Exception as e:
            print(e)
            session.rollback()
            raise e
        finally:
            if session:
                session.close()
        return id

    @staticmethod
    def verify(email:str, passwd:str):
        with db.auto_commit() as session:
            user = session.query(User).filter_by(email=email).first()
            if not user:
                raise ValueError('User not registered')
            if not user.check_password(passwd):
                raise ValueError('Password error')
            scope = 'AdminScope' if user.auth == AdminScope else 'UserScope'
            return {'uid': user.id, "scope": scope}

    def check_password(self, passwd:str):
        if not self._password:
            return False
        return check_password_hash(self._password, passwd)