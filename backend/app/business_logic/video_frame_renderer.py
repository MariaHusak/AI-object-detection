import cv2
import numpy as np

from app.business_logic.box_renderer import BoxRenderer
from app.business_logic.label_renderer import LabelRenderer

MASK_COLOR = (0, 255, 0)
MASK_ALPHA = 0.5


class VideoFrameRenderer:

    def __init__(self):
        self._box_renderer = BoxRenderer()
        self._label_renderer = LabelRenderer()

    def apply_segmentation(self, frame, mask_data, boxes, names, width, height):
        for i, mask in enumerate(mask_data):
            mask = self._resize_mask(mask, width, height)
            self._apply_mask_overlay(frame, mask)
            self._draw_box_and_label(frame, boxes, names, i)

    def apply_detections(self, frame, boxes, names):
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            conf = float(box.conf[0])
            label = names[int(box.cls[0])]
            self._box_renderer.draw(frame, (x1, y1, x2, y2), MASK_COLOR)
            self._label_renderer.draw(frame, f"{label} {conf:.2f}", x1, y1, MASK_COLOR)

    def _draw_box_and_label(self, frame, boxes, names, index):
        box = boxes.xyxy[index].cpu().numpy()
        conf = float(boxes.conf[index].cpu().numpy())
        label = names[int(boxes.cls[index].cpu().numpy())]
        x1, y1, x2, y2 = map(int, box)
        self._box_renderer.draw(frame, (x1, y1, x2, y2), MASK_COLOR)
        self._label_renderer.draw(frame, f"{label} {conf:.2f}", x1, y1, MASK_COLOR)

    def _resize_mask(self, mask, width, height):
        resized = cv2.resize(mask, (width, height))
        return resized > 0.5

    def _apply_mask_overlay(self, frame, mask):
        color = np.array(MASK_COLOR, dtype=np.uint8)
        frame[mask] = (frame[mask] * MASK_ALPHA + color * MASK_ALPHA).astype(np.uint8)