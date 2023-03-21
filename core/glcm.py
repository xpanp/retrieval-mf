import cv2
from cv2 import Mat
from typing import Union
import numpy as np
import torch
from skimage.feature import graycomatrix, graycoprops

from .utils import try_read_image

FEAT_DIM = 72


def glcm_calc(img: Union[str, Mat]) -> torch.Tensor:
    img = try_read_image(img)
    if img is None:
        return torch.empty(0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 计算灰度共生矩阵，参数：图像矩阵，步长，方向，灰度级别，是否对称，是否标准化
    # [0, np.pi / 4, np.pi / 2, np.pi * 3 / 4] 0、45、90、135度
    glcm = graycomatrix(img, [1, 2, 4], [
                        0, np.pi / 4, np.pi / 2, np.pi * 3 / 4], 256, symmetric=True, normed=True)

    features = []
    # 循环计算表征纹理的参数 对比度、相异性、同质性、能量、自相关、ASM能量
    for prop in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
        temp = graycoprops(glcm, prop)
        temp = np.array(temp).reshape(-1)
        features.extend(temp)
    return torch.Tensor(features)


class AlgoGLCM():
    def __init__(self) -> None:
        pass

    def forward_feature(self, img: Union[str, Mat]) -> torch.Tensor:
        return glcm_calc(img)
    
    def __call__(self, img: Union[str, Mat]) -> torch.Tensor:
        return self.forward_feature(img)
