import cv2
import sys
sys.path.append('../')

from core import color, glcm, lbp, vgg, vit, core_cfg
from utils.stat import timer


@timer
def feat_info(algo, img: str):
    feature = algo(img)
    print("len: ", len(feature))
    # assert(len(feature) == color.FEAT_DIM)

    print("dtype: ", feature.dtype)
    # assert(feature.dtype == torch.float32)

    print("shape: ", feature.shape)
    # assert(feature.shape == torch.Size([256]))

    # print(feature)


def test(algo):
    print("-----------------存在的图片")
    feat_info(algo, "1.jpg")
    print("\n-----------------不存在的图片")
    feat_info(algo, "unknown.jpg")
    print("\n-----------------从Mat加载")
    img = cv2.imread("1.jpg")
    feat_info(algo, img)


algo = color.AlgoColor()
test(algo)
algo = glcm.AlgoGLCM()
test(algo)
algo = lbp.AlgoLBP()
test(algo)
algo = vgg.AlgoVGG(cfg=core_cfg)
test(algo)
algo = vit.AlgoViT(cfg=core_cfg)
test(algo)
