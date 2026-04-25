import cv2


class ImageLoader:
    @staticmethod
    def load_rgba(path):
        image = cv2.imread(path)
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)