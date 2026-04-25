from app.core.model_loader import ModelLoader


class YOLOService:

    def __init__(self):
        self.model = ModelLoader.get_yolo()

    def detect(self, image_path):
        results = self.model(image_path)[0]
        return [self._parse_box(results, box) for box in results.boxes]

    def _parse_box(self, results, box):
        return {
            "class": self._get_class_name(results, box),
            "confidence": float(box.conf[0].item()),
            "box": box.xyxy[0].tolist()
        }

    def _get_class_name(self, results, box):
        cls_id = int(box.cls[0].item())
        return results.names[cls_id]