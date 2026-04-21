from app.services.yolo_service import YOLOService
from app.services.sam_service import SAMService
from app.domain.pipeline import AIPipeline


class PipelineFactory:

    @staticmethod
    def create():
        detector = YOLOService()
        segmenter = SAMService()

        return AIPipeline(detector, segmenter)
