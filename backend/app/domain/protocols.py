from typing import Protocol, runtime_checkable


@runtime_checkable
class Detector(Protocol):
    def detect(self, image_path: str) -> list: ...


@runtime_checkable
class Segmenter(Protocol):
    def segment(self, image_path: str, detections: list) -> list: ...