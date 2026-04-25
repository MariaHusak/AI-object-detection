import cv2


class BoxRenderer:

    def draw(self, image, box, color):
        x1, y1, x2, y2 = box

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            color,
            2
        )
