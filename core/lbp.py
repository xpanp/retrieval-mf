# copy from https://github.com/1044197988/Python-Image-feature-extraction.git
import cv2
from cv2 import Mat
from typing import Union
import numpy as np
import torch

from .utils import try_read_image

FEAT_DIM = 256

# revolve_map为旋转不变模式的36种特征值从小到大进行序列化编号得到的字典
revolve_map = {0: 0, 1: 1, 3: 2, 5: 3, 7: 4, 9: 5, 11: 6, 13: 7, 15: 8, 17: 9, 19: 10, 21: 11, 23: 12,
               25: 13, 27: 14, 29: 15, 31: 16, 37: 17, 39: 18, 43: 19, 45: 20, 47: 21, 51: 22, 53: 23,
               55: 24, 59: 25, 61: 26, 63: 27, 85: 28, 87: 29, 91: 30, 95: 31, 111: 32, 119: 33, 127: 34,
               255: 35}

# uniform_map为等价模式的58种特征值从小到大进行序列化编号得到的字典
uniform_map = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 6: 5, 7: 6, 8: 7, 12: 8,
               14: 9, 15: 10, 16: 11, 24: 12, 28: 13, 30: 14, 31: 15, 32: 16,
               48: 17, 56: 18, 60: 19, 62: 20, 63: 21, 64: 22, 96: 23, 112: 24,
               120: 25, 124: 26, 126: 27, 127: 28, 128: 29, 129: 30, 131: 31, 135: 32,
               143: 33, 159: 34, 191: 35, 192: 36, 193: 37, 195: 38, 199: 39, 207: 40,
               223: 41, 224: 42, 225: 43, 227: 44, 231: 45, 239: 46, 240: 47, 241: 48,
               243: 49, 247: 50, 248: 51, 249: 52, 251: 53, 252: 54, 253: 55, 254: 56,
               255: 57}


class AlgoLBP:
    def __init__(self) -> None:
        pass

    def forward_feature(self, img: Union[str, Mat]) -> torch.Tensor:
        img = try_read_image(img)
        if img is None:
            return torch.empty(0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        basic_array = self.lbp_basic(img)
        hist = self.get_hist(basic_array, [256], [0, 256])
        thist = torch.from_numpy(hist)
        return thist

    def __call__(self, img: Union[str, Mat]) -> torch.Tensor:
        return self.forward_feature(img)
    
    # 图像的LBP原始特征计算算法：将图像指定位置的像素与周围8个像素比较
    # 比中心像素大的点赋值为1，比中心像素小的赋值为0，返回得到的二进制序列
    def calute_basic_lbp(self, image_array, i, j):
        sum = []
        if image_array[i - 1, j - 1] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        if image_array[i - 1, j] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        if image_array[i - 1, j + 1] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        if image_array[i, j - 1] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        if image_array[i, j + 1] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        if image_array[i + 1, j - 1] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        if image_array[i + 1, j] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        if image_array[i + 1, j + 1] > image_array[i, j]:
            sum.append(1)
        else:
            sum.append(0)
        return sum

    # 获取二进制序列进行不断环形旋转得到新的二进制序列的最小十进制值
    def get_min_for_revolve(self, arr):
        values = []
        circle = arr
        circle.extend(arr)
        for i in range(0, 8):
            j = 0
            sum = 0
            bit_num = 0
            while j < 8:
                sum += circle[i + j] << bit_num
                bit_num += 1
                j += 1
            values.append(sum)
        return min(values)

    # 获取值r的二进制中1的位数
    def calc_sum(self, r):
        num = 0
        while (r):
            r &= (r - 1)
            num += 1
        return num

    # 获取图像的LBP原始模式特征
    # dim 256
    def lbp_basic(self, image_array):
        basic_array = np.zeros(image_array.shape, np.uint8)
        width = image_array.shape[0]
        height = image_array.shape[1]
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                sum = self.calute_basic_lbp(image_array, i, j)
                bit_num = 0
                result = 0
                for s in sum:
                    result += s << bit_num
                    bit_num += 1
                basic_array[i, j] = result
        return basic_array

    # 获取图像的LBP旋转不变模式特征
    # dim 36
    def lbp_revolve(self, image_array):
        revolve_array = np.zeros(image_array.shape, np.uint8)
        width = image_array.shape[0]
        height = image_array.shape[1]
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                sum = self.calute_basic_lbp(image_array, i, j)
                revolve_key = self.get_min_for_revolve(sum)
                revolve_array[i, j] = revolve_map[revolve_key]
        return revolve_array

    # 获取图像的LBP等价模式特征
    # dim 58
    def lbp_uniform(self, image_array):
        uniform_array = np.zeros(image_array.shape, np.uint8)
        basic_array = self.lbp_basic(image_array)
        width = image_array.shape[0]
        height = image_array.shape[1]

        for i in range(1, width - 1):
            for j in range(1, height - 1):
                k = basic_array[i, j] << 1
                if k > 255:
                    k = k - 255
                xor = basic_array[i, j] ^ k
                num = self.calc_sum(xor)
                if num <= 2:
                    uniform_array[i, j] = uniform_map[basic_array[i, j]]
                else:
                    uniform_array[i, j] = 58
        return uniform_array

    # 获取图像的LBP旋转不变等价模式特征
    def lbp_revolve_uniform(self, image_array):
        uniform_revolve_array = np.zeros(image_array.shape, np.uint8)
        basic_array = self.lbp_basic(image_array)
        width = image_array.shape[0]
        height = image_array.shape[1]
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                k = basic_array[i, j] << 1
                if k > 255:
                    k = k - 255
                xor = basic_array[i, j] ^ k
                num = self.calc_sum(xor)
                if num <= 2:
                    uniform_revolve_array[i, j] = self.calc_sum(
                        basic_array[i, j])
                else:
                    uniform_revolve_array[i, j] = 9
        return uniform_revolve_array

    def get_hist(self, img_array, im_bins, im_range):
        hist = cv2.calcHist([img_array], [0], None, im_bins, im_range)
        hist = cv2.normalize(hist, None).flatten()
        return hist
