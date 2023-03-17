import cv2
from cv2 import Mat
from typing import Union, Optional


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
        self.ALGO_WIDTH = cfg.ALGO_WIDTH
        self.ALGO_HEIGHT = cfg.ALGO_HEIGHT
        self.VGG_AVG_SIZE = cfg.VGG_AVG_SIZE
        self.VGG_MODEL = cfg.VGG_MODEL
        self.VIT_MODEL = cfg.VIT_MODEL
        self.VIT_EXTRACT_AVG = cfg.VIT_EXTRACT_AVG


core_cfg = CoreCFG()

ALGO_COLOR = "color"
ALGO_GLCM = "glcm"
ALGO_LBP = "lbp"
ALGO_VGG = "vgg"
ALGO_VIT = "vit"
