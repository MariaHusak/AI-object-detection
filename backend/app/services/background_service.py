import cv2
import numpy as np
import uuid
from pathlib import Path

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class BackgroundService:

    def replace_background(self, image_path, mask, new_bg_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        background = cv2.imread(new_bg_path)
        background = cv2.resize(background, (image.shape[1], image.shape[0]))
        background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA)

        mask = mask.astype(bool)

        result = background.copy()

        result[mask] = image[mask]

        filename = f"{uuid.uuid4()}_bg.png"
        output_path = OUTPUT_DIR / filename

        cv2.imwrite(str(output_path), result)

        return str(output_path)
