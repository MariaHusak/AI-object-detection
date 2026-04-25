import cv2


class LabelRenderer:

    def draw(self, image, text, x1, y1, color):
        cv2.putText(
            image,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )
