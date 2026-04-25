from app.business_logic.image_loader import ImageLoader
from app.business_logic.mask_service import MaskService
from app.business_logic.image_saver import ImageSaver


class CutoutService:

    def create_cutout(self, image_path, masks):
        image = ImageLoader.load_rgba(image_path)
        results = []

        for mask in masks:
            cutout = MaskService.apply(image, mask)
            results.append(ImageSaver.save_png(cutout))

        return results

    def create_combined_cutout(self, image_path, masks):
        image = ImageLoader.load_rgba(image_path)
        combined = MaskService.combine(masks)
        cutout = MaskService.apply(image, combined)

        return ImageSaver.save_png(cutout, "_combined")
