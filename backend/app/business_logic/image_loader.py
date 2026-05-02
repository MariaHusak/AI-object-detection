from PIL import Image, ImageOps
import numpy as np
import cv2


class ImageLoader:
    @staticmethod
    def load_rgba(path):
        image = Image.open(path)
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGBA")

        return np.array(image)

