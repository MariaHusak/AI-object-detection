import cv2
import uuid
from pathlib import Path


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class ImageSaver:

    @staticmethod
    def save_png(image, suffix=""):
        filename = f"{uuid.uuid4()}{suffix}.png"
        path = OUTPUT_DIR / filename

        cv2.imwrite(str(path), image)

        return str(path)