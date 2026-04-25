import numpy as np


class MaskService:

    @staticmethod
    def apply(image, mask):
        mask = mask.astype(bool)

        result = np.zeros_like(image)
        result[mask] = image[mask]
        result[~mask] = [0, 0, 0, 0]

        return result

    @staticmethod
    def combine(masks):
        combined = np.zeros(masks[0].shape, dtype=bool)

        for mask in masks:
            combined |= mask.astype(bool)

        return combined
