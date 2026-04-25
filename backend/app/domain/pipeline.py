from app.domain.protocols import Detector, Segmenter


class AIPipeline:
    def __init__(self, detector: Detector, segmenter: Segmenter):
        self.detector = detector
        self.segmenter = segmenter
