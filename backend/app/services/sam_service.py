import cv2
import numpy as np

from app.core.model_loader import ModelLoader


class SAMService:

    def __init__(self):
        self.predictor = ModelLoader.get_sam2()

    def segment(self, image_path, detections):
        self._load_image(image_path)
        return [self._predict_mask(det) for det in detections]

    def _load_image(self, image_path):
        image_bgr = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        self.predictor.set_image(image_rgb)

    def _predict_mask(self, det):
        box = np.array(det["box"])
        masks, _, _ = self.predictor.predict(
            point_coords=None,
            point_labels=None,
            box=box[None, :],
            multimask_output=False
        )
        return masks[0]