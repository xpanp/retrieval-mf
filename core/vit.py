import timm
import torch

from .model import Model
from . import *

FEAT_DIM = 768


class AlgoViT(Model):
    def __init__(self, cfg: CoreCFG):
        super().__init__(cfg)
        print("torch version:", torch.__version__)
        print("timm version:", timm.__version__)
        if timm.__version__ < '0.6':
            raise ValueError("Timm version should be at least 0.6.")
        self.model = self.get_model(cfg.VIT_MODEL, "")
        self.use_avg = cfg.VIT_EXTRACT_AVG
        print("use_avg:", self.use_avg)
        print(cfg.VIT_MODEL)
        print(self.transform)

    def get_model(self, model, ckp):
        return timm.create_model(model_name=model, pretrained=True)

    def postprocessing(self, feature):
        if timm.__version__ >= '0.6':
            # cls [batch, 197, 768] -> [batch, 768]
            if not self.use_avg:
                feature = feature[:, 0]
            else:
                # 平均池化
                feature = feature.transpose(1, 2)
                feature = torch.nn.AdaptiveAvgPool1d(1)(feature)
                feature = feature.squeeze(2)
        return feature
