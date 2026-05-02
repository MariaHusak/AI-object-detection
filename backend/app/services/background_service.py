import cv2
from app.business_logic.image_loader import ImageLoader
from app.business_logic.image_saver import ImageSaver


class BackgroundService:

    def replace_background(self, image_path, new_bg_path):
        foreground = ImageLoader.load_rgba(image_path)
        background = self._load_background(new_bg_path, foreground.shape)

        alpha = foreground[:, :, 3] > 0
        result = background.copy()
        result[alpha] = foreground[alpha]

        return ImageSaver.save_png(result, "_bg")

    def _load_background(self, bg_path, target_shape):
        background = ImageLoader.load_rgba(bg_path)
        height, width = target_shape[:2]
        return cv2.resize(background, (width, height))

    def _merge(self, foreground, background, mask):
        mask = mask.astype(bool)
        result = background.copy()
        result[mask] = foreground[mask]

        return result
