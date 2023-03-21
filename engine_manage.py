from utils import engine, config
from core import color, glcm, lbp, vgg, vit, AlgoType, core_cfg

class EngineManager:
    def __init__(self) -> None:
        self.engine_color = None
        self.engine_glcm = None
        self.engine_lbp = None
        self.engine_vgg = None
        self.engine_vit = None
        self.engine_map = None
        
    def init(self, cfg:config.RMFConfig) -> None:
        '''
            传统特征提取算法，多线程处理时不存在问题，
            仅为了保持接口一致方便调用
        '''
        engines = []
        for _ in range(cfg.NUM_WORKERS):
            algo = color.AlgoColor()
            engines.append(algo)
        self.engine_color = engine.EngineLock(engines)

        engines = []
        for _ in range(cfg.NUM_WORKERS):
            algo = glcm.AlgoGLCM()
            engines.append(algo)
        self.engine_glcm = engine.EngineLock(engines)

        engines = []
        for _ in range(cfg.NUM_WORKERS):
            algo = lbp.AlgoLBP()
            engines.append(algo)
        self.engine_lbp = engine.EngineLock(engines)

        '''
            深度学习算法，实际需要进行管理的对象
        '''
        core_cfg.parser(cfg)
        engines = []
        for _ in range(cfg.NUM_WORKERS):
            algo = vgg.AlgoVGG(core_cfg)
            engines.append(algo)
        self.engine_vgg = engine.EngineLock(engines)

        engines = []
        for _ in range(cfg.NUM_WORKERS):
            algo = vit.AlgoViT(core_cfg)
            engines.append(algo)
        self.engine_vit = engine.EngineLock(engines)

        '''
            引擎字典，便于通过算法名称来调用
        '''
        self.engine_map = {
            AlgoType.COLOR: self.engine_color,
            AlgoType.GLCM: self.engine_glcm,
            AlgoType.LBP: self.engine_lbp,
            AlgoType.VGG: self.engine_vgg,
            AlgoType.VIT: self.engine_vit,
        }
        print("EngineManager engine_map:", self.engine_map)
    
    def process(self, algo_name, data):
        return self.engine_map[algo_name](data)

    def __call__(self, algo_name, data):
        return self.process(algo_name, data)

engineM = EngineManager()