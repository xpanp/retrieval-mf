import cv2
from cv2 import Mat
from typing import Optional


def reduce(src:Mat, dst_size:int) -> Optional[Mat]:
    '''
        保持比例缩放，短边缩放至dst_size
        若不需要缩放则返回None，否则返回缩放好的Mat
    '''
    height = src.shape[0]
    width = src.shape[1]
    if dst_size * 2 > min(width, height):
        # 原图本来就很小，不需要缩放
        return None

    print(f'width: {width} height: {height}')
    if width < height:
        ratio = dst_size / float(src.shape[1])
        width = dst_size
        height = int(src.shape[0] * ratio)
    else:
        ratio = dst_size / float(src.shape[0])
        height = dst_size
        width = int(src.shape[1] * ratio)
    print(f'width: {width} height: {height} ratio: {ratio}')
    dst_image = cv2.resize(src, (width, height), interpolation=cv2.INTER_CUBIC)
    return dst_image