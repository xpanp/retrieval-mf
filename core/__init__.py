import cv2
from cv2 import Mat
from typing import Union, Optional
from enum import Enum


def try_read_image(img: Union[str, Mat]) -> Optional[Mat]:
    # 将图片路径转换为Mat
    if isinstance(img, str):
        img = cv2.imread(img)
    return img


class CoreCFG:
    ALGO_RESIZE = 248
    ALGO_WIDTH = 224
    ALGO_HEIGHT = 224
    VGG_AVG_SIZE = 7
    VGG_MODEL = "vgg16"
    VIT_MODEL = "vit_base_patch16_224"
    VIT_EXTRACT_AVG = False

    def __init__(self) -> None:
        pass

    def parser(self, cfg):
        self.ALGO_RESIZE = cfg.ALGO_RESIZE
        self.ALGO_WIDTH = cfg.ALGO_RESIZE
        self.ALGO_HEIGHT = cfg.ALGO_RESIZE
        self.VGG_AVG_SIZE = cfg.ALGO_RESIZE
        self.VGG_MODEL = cfg.ALGO_RESIZE
        self.VIT_MODEL = cfg.ALGO_RESIZE
        self.VIT_EXTRACT_AVG = cfg.ALGO_RESIZE


core_cfg = CoreCFG()


class AlgoName(Enum):
    COLOR = "color"
    GLCM = "glcm"
    LBP = "lbp"
    VGG = "vgg"
    VIT = "vit"
