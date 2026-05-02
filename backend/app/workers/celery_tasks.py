from app.core.celery_app import celery_app
from app.services.video_service import VideoService

video_service = VideoService()


@celery_app.task(bind=True)
def process_video_task(self, video_path: str):

    result_path = video_service.process_video(video_path)

    return {
        "video": result_path
    }
