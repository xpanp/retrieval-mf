import configparser
import os


class RMFConfig:
    HOST = "0.0.0.0"
    PORT = 8000
    NUM_WORKERS = 1
    # cpu -1, others gpuid
    CUDA_VISIBLE_DEVICES = 0
    DEBUG = False
    TMP_DIR = "tmp"
    FILE_SERVER_URL = "http://127.0.0.1:8001/"

    ALGO_RESIZE = 248
    ALGO_WIDTH = 224
    ALGO_HEIGHT = 224
    VGG_AVG_SIZE = 7
    VGG_MODEL = "vgg16"
    VIT_MODEL = "vit_base_patch16_224"
    VIT_EXTRACT_AVG = False

    # support milvus|cosine
    CMP_MODE = "milvus"
    # 同步模式，若开启，则删除现有milvus库，使用mysql中的数据重新建库
    SYNC_MILVUS = False

    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWD = "LWsVjzKIO0FTdA=="
    DB_NAME = "rmf"

    MILVUS_HOST = "127.0.0.1"
    MILVUS_PORT = 19530

    def __init__(self) -> None:
        # DSN Data Source Name
        self.DSN = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
            self.DB_USER, self.DB_PASSWD, self.DB_HOST, self.DB_PORT, self.DB_NAME
        )

    def parser(self, cfg: str):
        '''
            使用配置文件覆盖默认参数
        '''
        config = configparser.ConfigParser()
        config.read(cfg, encoding='utf-8')
        print("read cfg: ", cfg)

        self.HOST = config.get("server", "HOST", fallback=self.HOST)
        self.PORT = config.getint("server", "PORT", fallback=self.PORT)
        self.NUM_WORKERS = config.getint(
            "server", "NUM_WORKERS", fallback=self.NUM_WORKERS)
        self.CUDA_VISIBLE_DEVICES = config.getint(
            "server", "CUDA_VISIBLE_DEVICES", fallback=self.CUDA_VISIBLE_DEVICES)
        self.DEBUG = config.getboolean("server", "DEBUG", fallback=self.DEBUG)
        self.TMP_DIR = config.get("server", "TMP_DIR", fallback=self.TMP_DIR)
        self.FILE_SERVER_URL = config.get("server", "FILE_SERVER_URL", fallback=self.FILE_SERVER_URL)
        
        self.ALGO_RESIZE = config.getint("engine", "ALGO_RESIZE", fallback=self.ALGO_RESIZE)
        self.ALGO_WIDTH = config.getint("engine", "ALGO_WIDTH", fallback=self.ALGO_WIDTH)
        self.ALGO_HEIGHT = config.getint("engine", "ALGO_HEIGHT", fallback=self.ALGO_HEIGHT)
        self.VGG_AVG_SIZE = config.getint("engine", "VGG_AVG_SIZE", fallback=self.VGG_AVG_SIZE)
        self.VGG_MODEL = config.get("engine", "VGG_MODEL", fallback=self.VGG_MODEL)
        self.VIT_MODEL = config.get("engine", "VIT_MODEL", fallback=self.VIT_MODEL)
        self.VIT_EXTRACT_AVG = config.getboolean(
            "engine", "VIT_EXTRACT_AVG", fallback=self.VIT_EXTRACT_AVG)
        
        self.CMP_MODE = config.get("compare", "CMP_MODE", fallback=self.CMP_MODE)
        self.SYNC_MILVUS = config.getboolean("compare", "SYNC_MILVUS", fallback=self.SYNC_MILVUS)

        self.DB_HOST = config.get("db", "DB_HOST", fallback=self.DB_HOST)
        self.DB_PORT = config.getint("db", "DB_PORT", fallback=self.DB_PORT)
        self.DB_USER = config.get("db", "DB_USER", fallback=self.DB_USER)
        self.DB_PASSWD = config.get("db", "DB_PASSWD", fallback=self.DB_PASSWD)
        self.DB_NAME = config.get("db", "DB_NAME", fallback=self.DB_NAME)
        # DSN Data Source Name
        self.DSN = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
            self.DB_USER, self.DB_PASSWD, self.DB_HOST, self.DB_PORT, self.DB_NAME
        )

        self.MILVUS_HOST = config.get("milvus", "MILVUS_HOST", fallback=self.MILVUS_HOST)
        self.MILVUS_PORT = config.getint("milvus", "MILVUS_PORT", fallback=self.MILVUS_PORT)

        self.init_dir()

    def init_dir(self):
        if not os.path.exists(self.TMP_DIR):
            os.makedirs(self.TMP_DIR)


cfg = RMFConfig()
