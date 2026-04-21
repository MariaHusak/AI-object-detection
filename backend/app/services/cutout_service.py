import cv2
import numpy as np
import uuid
from pathlib import Path

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class CutoutService:

    def create_cutout(self, image_path, masks, detections):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        results = []

        for i, (mask, det) in enumerate(zip(masks, detections)):

            mask = mask.astype(bool)

            cutout = np.zeros_like(image)

            cutout[mask] = image[mask]

            cutout[~mask] = [0, 0, 0, 0]

            filename = f"{uuid.uuid4()}.png"
            output_path = OUTPUT_DIR / filename

            cv2.imwrite(str(output_path), cutout)

            results.append(str(output_path))

        return results


    def create_combined_cutout(self, image_path, masks):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        combined_mask = np.zeros(image.shape[:2], dtype=bool)

        # об'єднуємо всі маски
        for mask in masks:
            combined_mask = combined_mask | mask.astype(bool)

        cutout = np.zeros_like(image)

        cutout[combined_mask] = image[combined_mask]
        cutout[~combined_mask] = [0, 0, 0, 0]

        filename = f"{uuid.uuid4()}_combined.png"
        output_path = OUTPUT_DIR / filename

        cv2.imwrite(str(output_path), cutout)

        return str(output_path)

