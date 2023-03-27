import cv2
from cv2 import Mat
from typing import Union, Optional


def try_read_image(img: Union[str, Mat]) -> Optional[Mat]:
    # 将图片路径转换为Mat
    if isinstance(img, str):
        img = cv2.imread(img)
    return img


def reduce(src: Mat, dst_size: int) -> Optional[Mat]:
    '''
        保持比例缩放，短边缩放至dst_size
        若不需要缩放则返回None，否则返回缩放好的Mat
    '''
    height = src.shape[0]
    width = src.shape[1]
    if dst_size * 2 > min(width, height):
        # 原图本来就很小，不需要缩放
        return None

    print(f'raw width: {width}, raw height: {height}')
    if width < height:
        ratio = dst_size / float(src.shape[1])
        width = dst_size
        height = int(src.shape[0] * ratio)
    else:
        ratio = dst_size / float(src.shape[0])
        height = dst_size
        width = int(src.shape[1] * ratio)
    print(f'dst width: {width}, dst height: {height}, ratio: {ratio}')
    dst_image = cv2.resize(src, (width, height), interpolation=cv2.INTER_CUBIC)
    return dst_image


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
