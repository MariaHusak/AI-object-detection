import numpy as np
import cv2


class MaskService:

    @staticmethod
    def apply(image, mask):
        mask = cv2.resize(
            mask.astype(np.uint8),
            (image.shape[1], image.shape[0])
        ).astype(bool)
        h, w = image.shape[:2]
        result = np.zeros((h, w, 4), dtype=np.uint8)
        result[mask] = image[mask]
        result[~mask] = [0, 0, 0, 0]

        return result

    @staticmethod
    def combine(masks):
        combined = np.zeros(masks[0].shape, dtype=bool)

        for mask in masks:
            combined |= mask.astype(bool)

        return combined
