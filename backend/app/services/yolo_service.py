from app.core.model_loader import ModelLoader


class YOLOService:

    def __init__(self):
        self.model = ModelLoader.get_yolo()

    def detect(self, image_path):
        results = self.model(image_path)[0]

        detections = []

        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            cls_id = int(box.cls[0].item())
            class_name = results.names[cls_id]

            conf = float(box.conf[0].item())

            detections.append({
                "class": class_name,
                "confidence": conf,
                "box": [x1, y1, x2, y2]
            })

        return detections
