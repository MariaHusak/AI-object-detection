import cv2
import uuid
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class DrawService:

    def draw_boxes(self, image_path, detections):
        image = cv2.imread(image_path)

        for det in detections:
            x1, y1, x2, y2 = map(int, det["box"])

            label = det.get("class", det.get("name", "object"))
            conf = det.get("confidence", 0)

            color = (0, 255, 0)

            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            text = f"{label} {conf:.2f}"

            cv2.putText(
                image,
                text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        filename = f"{uuid.uuid4()}.jpg"
        output_path = OUTPUT_DIR / filename

        cv2.imwrite(str(output_path), image)

        return str(output_path)

    def draw_segmentation(self, image_path, detections, masks):
        image = cv2.imread(image_path)
        overlay = image.copy()

        for det, mask in zip(detections, masks):

            x1, y1, x2, y2 = map(int, det["box"])

            color = (
                int(np.random.randint(50, 255)),
                int(np.random.randint(50, 255)),
                int(np.random.randint(50, 255))
            )

            mask_bool = mask.astype(bool)

            overlay[mask_bool] = color

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            label = det["class"]
            conf = det["confidence"]

            text = f"{label} {conf:.2f}"

            cv2.putText(
                image,
                text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        result = cv2.addWeighted(
            overlay,
            0.35,
            image,
            0.65,
            0
        )

        filename = f"{uuid.uuid4()}.jpg"
        output_path = OUTPUT_DIR / filename

        cv2.imwrite(str(output_path), result)

        return str(output_path)
