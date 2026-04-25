import cv2


class MaskRenderer:

    def apply(self, image, mask, color):
        channels = image.shape[2] if image.ndim == 3 else 1
        if channels == 4 and len(color) == 3:
            color = (*color, 255)
        image[mask.astype(bool)] = color

    def blend(self, overlay, image):
        return cv2.addWeighted(overlay, 0.35, image, 0.65, 0)