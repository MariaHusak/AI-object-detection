import numpy as np
from pathlib import Path
from app.business_logic.image_loader import ImageLoader
from app.business_logic.image_saver import ImageSaver
from app.business_logic.color_service import ColorService
from app.business_logic.box_renderer import BoxRenderer
from app.business_logic.label_renderer import LabelRenderer
from app.business_logic.mask_renderer import MaskRenderer


class DrawService:
    def __init__(self):
        self._color_service = ColorService()
        self._box_renderer = BoxRenderer()
        self._label_renderer = LabelRenderer()
        self._mask_renderer = MaskRenderer()

    def draw_boxes(self, image_path, detections):
        image = ImageLoader.load_rgba(image_path)

        for det in detections:
            color = self._color_service.default()
            self._draw_detection(image, det, color)

        saved_path = ImageSaver.save_png(image)

        return self._to_public_url(saved_path)

    def draw_segmentation(self, image_path, detections, masks):
        image = ImageLoader.load_rgba(image_path)
        overlay = image.copy()

        for det, mask in zip(detections, masks):
            color = self._color_service.random()
            self._mask_renderer.apply(overlay, mask, color)
            self._draw_detection(image, det, color)

        result = self._mask_renderer.blend(overlay, image)

        saved_path = ImageSaver.save_png(result)

        return self._to_public_url(saved_path)

    def _draw_detection(self, image, det, color):
        x1, y1, x2, y2 = map(int, det["box"])
        self._box_renderer.draw(image, (x1, y1, x2, y2), color)

    def _format_label(self, det):
        label = det.get("class", det.get("name", "object"))
        conf = det.get("confidence", 0)
        return f"{label} {conf:.2f}"

    def _to_public_url(self, file_path: str) -> str:
        filename = Path(file_path).name
        return f"http://localhost:8000/outputs/{filename}"

