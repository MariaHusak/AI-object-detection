import os
import torch
import logging
from app.core.celery_app import celery_app
from app.services.video_service import VideoService

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
torch.set_num_threads(1)


logger = logging.getLogger(__name__)

video_service = VideoService()


@celery_app.task(bind=True)
def process_video_task(self, video_path: str):
    logger.info(f"Starting video processing: {video_path}")
    result_path = video_service.process_video(video_path)
    logger.info(f"Finished video processing: {result_path}")

    return {
        "video": result_path
    }
