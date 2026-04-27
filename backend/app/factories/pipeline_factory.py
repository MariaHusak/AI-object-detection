from app.services.yolo_service import YOLOService
from app.services.sam_service import SAMService
from app.domain.pipeline import AIPipeline


class PipelineFactory:

    @staticmethod
    def create() -> AIPipeline:
        return AIPipeline(
            detector=YOLOService(),
            segmenter=SAMService()
        )
