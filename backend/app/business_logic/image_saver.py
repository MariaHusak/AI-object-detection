import cv2
import uuid
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

class ImageSaver:

    @staticmethod
    def save_png(image, suffix=""):
        filename = f"{uuid.uuid4()}{suffix}.png"
        path = OUTPUT_DIR / filename

        if image.shape[2] == 4:
            image_to_save = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
        else:
            image_to_save = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imwrite(str(path), image_to_save)

        return str(path)