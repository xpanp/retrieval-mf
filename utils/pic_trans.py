from typing import List
from pathlib import Path


img_extensions = ['jpg', 'jpeg', 'png', 'bmp']


def get_img_files(dir: Path) -> List[Path]:
    '''
        递归遍历文件夹，获取图片文件列表
    '''
    img_files = []
    for file_path in dir.rglob("*"):
        if not file_path.is_file():
            continue
        '''
            .suffix方法返回的文件后缀包含'.'
            如 "test.jpg", 返回".jpg", 因此要去掉 '.'
        '''
        if file_path.suffix.lower()[1:] in img_extensions:
            img_files.append(file_path)
    return img_files
