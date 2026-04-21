import cv2
import uuid
import numpy as np
from pathlib import Path

from app.core.model_loader import ModelLoader


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class VideoService:

    def __init__(self):
        self.yolo = ModelLoader.get_yolo()

    def process_video(self, video_path: str):
        cap = cv2.VideoCapture(video_path)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        output_path = OUTPUT_DIR / f"{uuid.uuid4()}.mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            str(output_path),
            fourcc,
            fps,
            (width, height)
        )

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # YOLO detection / segmentation
            results = self.yolo(rgb)[0]

            boxes = results.boxes
            masks = results.masks

            # -----------------------------------
            # якщо є маски (segmentation model)
            # -----------------------------------
            if masks is not None:

                mask_data = masks.data.cpu().numpy()

                for i, mask in enumerate(mask_data):

                    # resize mask до розміру кадру
                    mask = cv2.resize(
                        mask,
                        (width, height)
                    )

                    mask = mask > 0.5

                    color = np.array(
                        (0, 255, 0),
                        dtype=np.uint8
                    )

                    # overlay
                    frame[mask] = (
                        frame[mask] * 0.5 +
                        color * 0.5
                    ).astype(np.uint8)

                    # bbox
                    box = boxes.xyxy[i].cpu().numpy()
                    conf = float(boxes.conf[i].cpu().numpy())
                    cls = int(boxes.cls[i].cpu().numpy())

                    label = self.yolo.names[cls]

                    x1, y1, x2, y2 = map(int, box)

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    text = f"{label} {conf:.2f}"

                    cv2.putText(
                        frame,
                        text,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

            # -----------------------------------
            # якщо segmentation masks нема
            # тоді просто bbox mode
            # -----------------------------------
            else:

                for box in boxes:

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0].cpu().numpy()
                    )

                    conf = float(box.conf[0])
                    cls = int(box.cls[0])

                    label = self.yolo.names[cls]

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    text = f"{label} {conf:.2f}"

                    cv2.putText(
                        frame,
                        text,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

            out.write(frame)

        cap.release()
        out.release()

        return str(output_path)
