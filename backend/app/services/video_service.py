import cv2
import logging
from app.core.model_loader import ModelLoader
from app.business_logic.video_frame_renderer import VideoFrameRenderer
from app.business_logic.video_saver import VideoSaver

logger = logging.getLogger(__name__)


class VideoService:

    def __init__(self):
        self.yolo = ModelLoader.get_yolo()
        self._renderer = VideoFrameRenderer()

    def process_video(self, video_path: str):
        logger.info(f"Opening video: {video_path}")
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            logger.error(f"Cannot open video: {video_path}")
            raise RuntimeError(f"Cannot open video file: {video_path}")

        logger.info(f"Video opened, frames: {int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}")

        out, temp_path, final_path = VideoSaver.create_writer(
            *self._get_frame_size(cap),
            self._get_fps(cap)
        )

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            self._process_frame(frame, out)
            frame_count += 1
            if frame_count % 10 == 0:
                logger.info(f"Processed {frame_count} frames")

        logger.info(f"Done, total frames: {frame_count}")
        cap.release()
        out.release()

        return VideoSaver.convert_to_h264(temp_path, final_path)

    def _process_frame(self, frame, out):
        results = self.yolo(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))[0]
        self._render_results(frame, results)
        out.write(frame)

    def _render_results(self, frame, results):
        if results.masks is not None:
            self._renderer.apply_segmentation(
                frame,
                results.masks.data.cpu().numpy(),
                results.boxes,
                self.yolo.names,
                *self._get_frame_size_from_frame(frame)
            )
        else:
            self._renderer.apply_detections(frame, results.boxes, self.yolo.names)

    @staticmethod
    def _get_fps(cap):
        return int(cap.get(cv2.CAP_PROP_FPS))

    @staticmethod
    def _get_frame_size(cap):
        return int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @staticmethod
    def _get_frame_size_from_frame(frame):
        return frame.shape[1], frame.shape[0]