from ultralytics import YOLO
import torch
import os

from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor


class ModelLoader:
    _yolo = None
    _sam2 = None

    @classmethod
    def get_yolo(cls):
        if cls._yolo is None:
            cls._yolo = YOLO("models/best.pt")
        return cls._yolo

    @classmethod
    def get_sam2(cls):
        if cls._sam2 is None:

            device = "cuda" if torch.cuda.is_available() else "cpu"

            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.dirname(__file__))
            )

            config_path = os.path.join(
                BASE_DIR,
                "segment-anything-2",
                "sam2",
                "configs",
                "sam2.1",
                "sam2.1_hiera_s.yaml"
            )

            checkpoint_path = os.path.join(
                BASE_DIR,
                "models",
                "sam2.1_hiera_small.pt"
            )

            model = build_sam2(
                config_path,
                checkpoint_path,
                device=device
            )

            cls._sam2 = SAM2ImagePredictor(model)

        return cls._sam2
