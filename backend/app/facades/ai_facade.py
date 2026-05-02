from app.factories.pipeline_factory import PipelineFactory
from app.services.draw_service import DrawService
from app.services.cutout_service import CutoutService
from app.services.background_service import BackgroundService
from app.services.video_service import VideoService
from app.business_logic.mask_service import MaskService

from app.workers.celery_tasks import process_video_task
from celery.result import AsyncResult
from app.core.celery_app import celery_app
import os

BASE_URL = "http://localhost:8000"


class AIFacade:

    def __init__(self):
        self.pipeline = PipelineFactory.create()
        self.drawer = DrawService()
        self.cutter = CutoutService()
        self.bg_service = BackgroundService()
        self.video_service = VideoService()

    def detect(self, image_path):
        return self.pipeline.detector.detect(image_path)

    def detect_preview(self, image_path):
        detections = self.detect(image_path)

        image_url = self.drawer.draw_boxes(image_path, detections)

        return {
            "image_url": image_url,
            "boxes": self._format_boxes(detections)
        }

    def segment_preview(self, image_path, selected_indices=None):
        detections, masks = self._detect_and_segment(
            image_path, selected_indices)
        result = self.drawer.draw_segmentation(
            image_path, detections, masks)
        return {
            "result_image": result,
            "detections": self._format_boxes(detections)
        }

    def cutout(self, image_path, selected_indices=None, mode="multi"):
        detections, masks = self._detect_and_segment(image_path, selected_indices)
        result = self._create_cutout_by_mode(image_path, masks, mode)
        cutouts = result.get("cutouts") or [result.get("cutout")]
        cutouts = [self._to_url(c) for c in cutouts if c]

        return {
            "image_url": self.drawer._to_public_url(
                self.drawer.draw_boxes(image_path, detections)
            ),
            "cutouts": cutouts,
            "detections": self._format_boxes(detections)
        }

    def replace_background(self, image_path, bg_path):
        result = self.bg_service.replace_background(image_path, bg_path)
        return {"result_image": self._to_url(result)}

    def process_video(self, video_path):
        return {"video": self.video_service.process_video(video_path)}

    def process_video_async(self, video_path):
        task = process_video_task.delay(video_path)
        return {"task_id": task.id}

    def get_task_status(self, task_id: str):
        task = AsyncResult(task_id, app=celery_app)
        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None
        }

    def _detect_and_segment(self, image_path, selected_indices=None):
        detections = self.detect(image_path)
        detections = self._filter_detections(detections, selected_indices)
        masks = self.pipeline.segmenter.segment(image_path, detections)
        return detections, masks

    def _filter_detections(self, detections, selected_indices):
        if not selected_indices:
            return detections
        return [det for i, det in enumerate(detections) if i in selected_indices]

    def _create_cutout_by_mode(self, image_path, masks, mode):
        if mode in ["single", "multi"]:
            return {"cutouts": self.cutter.create_cutout(image_path, masks)}
        elif mode == "combined":
            return {"cutout": self.cutter.create_combined_cutout(image_path, masks)}

    def _format_boxes(self, detections):
        formatted = []
        for det in detections:
            x1, y1, x2, y2 = det["box"]
            formatted.append({
                "x": int(x1),
                "y": int(y1),
                "w": int(x2 - x1),
                "h": int(y2 - y1),
                "label": det["class"],
                "conf": det["confidence"]
            })

        return formatted

    def _to_url(self, path: str):
        return BASE_URL + "/" + path.replace("\\", "/")



