import cv2
import numpy as np

from app.core.model_loader import ModelLoader


class SAMService:

    def __init__(self):
        self.predictor = ModelLoader.get_sam2()

    def segment(self, image_path, detections):
        image_bgr = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        self.predictor.set_image(image_rgb)

        masks = []

        for det in detections:
            box = np.array(det["box"])

            result_masks, scores, _ = self.predictor.predict(
                point_coords=None,
                point_labels=None,
                box=box[None, :],
                multimask_output=False
            )

            masks.append(result_masks[0])

        return masks
