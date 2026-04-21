from app.factories.pipeline_factory import PipelineFactory
from app.services.draw_service import DrawService
from app.services.cutout_service import CutoutService
from app.services.background_service import BackgroundService
from app.services.video_service import VideoService

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

        return self.drawer.draw_boxes(
            image_path,
            detections
        )

    def segment_preview(self, image_path, selected_indices=None):
        detections = self.detect(image_path)

        if selected_indices is not None and len(selected_indices) > 0:
            detections = [
                det for i, det in enumerate(detections)
                if i in selected_indices
            ]

        masks = self.pipeline.segmenter.segment(
            image_path,
            detections
        )

        result = self.drawer.draw_segmentation(
            image_path,
            detections,
            masks
        )

        return {
            "detections": detections,
            "result_image": result
        }

    def cutout(self, image_path, selected_indices=None, mode="multi"):
        detections = self.detect(image_path)

        if selected_indices is not None:
            detections = [
                det for i, det in enumerate(detections)
                if i in selected_indices
            ]

        masks = self.pipeline.segmenter.segment(
            image_path,
            detections
        )

        if mode == "single":
            return {
                "cutouts": self.cutter.create_cutout(
                    image_path,
                    masks,
                    detections
                )
            }

        elif mode == "multi":
            return {
                "cutouts": self.cutter.create_cutout(
                    image_path,
                    masks,
                    detections
                )
            }

        elif mode == "combined":
            return {
                "cutout": self.cutter.create_combined_cutout(
                    image_path,
                    masks
                )
            }

    def replace_background(self, image_path, bg_path, selected_indices=None):
        detections = self.detect(image_path)

        if selected_indices is not None:
            detections = [
                det for i, det in enumerate(detections)
                if i in selected_indices
            ]

        masks = self.pipeline.segmenter.segment(
            image_path,
            detections
        )

        combined_mask = masks[0].astype(bool)

        for m in masks[1:]:
            combined_mask = combined_mask | m.astype(bool)

        result = self.bg_service.replace_background(
            image_path,
            combined_mask,
            bg_path
        )

        return {
            "result_image": result
        }

    def process_video(self, video_path):
        return {
            "video": self.video_service.process_video(video_path)
        }

    def process_video_async(self, video_path):
        task = process_video_task.delay(video_path)

        return {
            "task_id": task.id
        }

    def get_task_status(self, task_id: str):
        task = AsyncResult(task_id, app=celery_app)

        return {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.ready() else None
        }
