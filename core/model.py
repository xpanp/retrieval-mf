from abc import ABC, abstractmethod
from PIL import Image
from torchvision import transforms
import torch
import cv2
from cv2 import Mat
from typing import Union

from .utils import CoreCFG, try_read_image

def l2n(x, eps=1e-6):
    return x / (torch.norm(x, p=2, dim=1, keepdim=True) + eps).expand_as(x)


class Model(ABC):
    def __init__(self, cfg: CoreCFG):
        # 应当根据数据特性设置transforms
        self.transform = transforms.Compose([
            transforms.Resize(
                size=cfg.ALGO_RESIZE, interpolation=transforms.InterpolationMode.BICUBIC),
            transforms.CenterCrop(size=(cfg.ALGO_WIDTH, cfg.ALGO_HEIGHT)),
            transforms.ToTensor(),
            # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            transforms.Normalize(mean=[0.5000, 0.5000, 0.5000], std=[
                                 0.5000, 0.5000, 0.5000])
        ])
        self.model = None

    @abstractmethod
    def get_model(self, model, ckp):
        pass

    def postprocessing(self, feature):
        return feature

    def forward_feature(self, img: Union[str, Mat]) -> torch.Tensor:
        img = try_read_image(img)
        if img is None:
            return torch.empty(0)
        # 将cv2的Mat转换为PIL.Image
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # timm的forward_features支持多图同时推理
        # 这里我们只有一张图片，因此需要先增加一个图片数量的维度，最后再去除
        img_tensor = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            feature = self.model.forward_features(img_tensor)
        feature = self.postprocessing(feature)
        feature = feature.squeeze(0)
        return feature

    def __call__(self, img: Union[str, Mat]) -> torch.Tensor:
        return self.forward_feature(img)
