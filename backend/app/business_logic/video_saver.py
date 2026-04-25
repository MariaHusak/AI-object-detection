import cv2
import uuid
from pathlib import Path

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class VideoSaver:

    @staticmethod
    def create_writer(width, height, fps, suffix=""):
        filename = f"{uuid.uuid4()}{suffix}.mp4"
        path = OUTPUT_DIR / filename
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
        return writer, str(path)