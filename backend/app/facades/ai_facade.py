from app.factories.pipeline_factory import PipelineFactory
from app.services.draw_service import DrawService
from app.services.cutout_service import CutoutService
from app.services.background_service import BackgroundService
from app.services.video_service import VideoService
from app.business_logic.mask_service import MaskService

from app.workers.celery_tasks import process_video_task
from celery.result import AsyncResult
from app.core.celery_app import celery_app


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
        return self.drawer.draw_boxes(image_path, detections)

    def segment_preview(self, image_path, selected_indices=None):
        detections, masks = self._detect_and_segment(image_path, selected_indices)
        result = self.drawer.draw_segmentation(image_path, detections, masks)
        return {"detections": detections, "result_image": result}

    def cutout(self, image_path, selected_indices=None, mode="multi"):
        _, masks = self._detect_and_segment(image_path, selected_indices)
        return self._create_cutout_by_mode(image_path, masks, mode)

    def replace_background(self, image_path, bg_path, selected_indices=None):
        _, masks = self._detect_and_segment(image_path, selected_indices)
        combined_mask = MaskService.combine(masks)
        result = self.bg_service.replace_background(image_path, combined_mask, bg_path)
        return {"result_image": result}

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