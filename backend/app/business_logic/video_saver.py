import cv2
import uuid
import subprocess
from pathlib import Path
import imageio_ffmpeg

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class VideoSaver:

    @staticmethod
    def create_writer(width, height, fps, suffix=""):
        filename = f"{uuid.uuid4()}{suffix}"
        temp_path = OUTPUT_DIR / f"{filename}_tmp.mp4"
        final_path = OUTPUT_DIR / f"{filename}.mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(temp_path), fourcc, fps, (width, height))
        return writer, str(temp_path), str(final_path)

    @staticmethod
    def convert_to_h264(temp_path: str, final_path: str):
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        result = subprocess.run([
            ffmpeg_exe, "-y",
            "-i", temp_path,
            "-vcodec", "libx264",
            "-crf", "23",
            "-preset", "fast",
            final_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr}")

        Path(temp_path).unlink()
        return final_path