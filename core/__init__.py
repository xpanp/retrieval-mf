from enum import Enum

from . import color
from . import glcm
from . import lbp
from . import vgg
from . import vit
from .utils import CoreCFG

core_cfg = CoreCFG()

class AlgoType(Enum):
    COLOR = "color"
    GLCM = "glcm"
    LBP = "lbp"
    VGG = "vgg"
    VIT = "vit"
    FUSION = "fusion"

algo_list = [AlgoType.COLOR, AlgoType.GLCM, AlgoType.LBP, AlgoType.VGG, AlgoType.VIT]

algo_dim_map = {
    AlgoType.COLOR: color.FEAT_DIM,
    AlgoType.GLCM: glcm.FEAT_DIM,
    AlgoType.LBP: lbp.FEAT_DIM,
    AlgoType.VGG: vgg.FEAT_DIM,
    AlgoType.VIT: vit.FEAT_DIM,
}

def get_dim(algo:AlgoType) -> int:
    return algo_dim_map[algo]

