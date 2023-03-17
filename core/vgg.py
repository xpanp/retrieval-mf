import torch
import timm

from .model import Model
from . import *

FEAT_DIM = 512


class AlgoVGG(Model):
    def __init__(self, cfg: CoreCFG):
        super().__init__(cfg)
        print("torch version:", torch.__version__)
        print("timm version:", timm.__version__)
        self.model = self.get_model(cfg.VGG_MODEL, "")
        # 最后一层特征图做平均池化
        self.avg = torch.nn.AvgPool2d(cfg.VGG_AVG_SIZE, stride=1)
        print(cfg.VGG_MODEL)
        print(self.transform)

    def get_model(self, model, ckp):
        return timm.create_model(model_name=model, pretrained=True)

    def postprocessing(self, feature):
        # torch.Size([1, 512, 7, 7])
        feature = self.avg(feature)
        # torch.Size([1, 512, 1, 1])
        feature = feature.view(1, -1)
        # torch.Size([1, 512])
        return feature
