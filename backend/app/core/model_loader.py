from pathlib import Path
import torch

_original_torch_load = torch.load

def _patched_torch_load(f, *args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _original_torch_load(f, *args, **kwargs)

torch.load = _patched_torch_load

from ultralytics import YOLO
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor


BASE_DIR = Path(__file__).resolve().parent.parent.parent

YOLO_MODEL_PATH = "models/best.pt"
SAM2_CONFIG = "sam2.1/sam2.1_hiera_s"
SAM2_CHECKPOINT_PATH = BASE_DIR / "models" / "sam2.1_hiera_small.pt"


class ModelLoader:
    _yolo = None
    _sam2 = None

    @classmethod
    def get_yolo(cls):
        if cls._yolo is None:
            cls._yolo = YOLO(YOLO_MODEL_PATH)
        return cls._yolo

    @classmethod
    def get_sam2(cls):
        if cls._sam2 is None:
            cls._sam2 = cls._build_sam2()
        return cls._sam2

    @classmethod
    def _build_sam2(cls):
        model = build_sam2(
            SAM2_CONFIG,
            str(SAM2_CHECKPOINT_PATH),
            device=cls._get_device()
        )
        return SAM2ImagePredictor(model)

    @staticmethod
    def _get_device():
        return "cuda" if torch.cuda.is_available() else "cpu"