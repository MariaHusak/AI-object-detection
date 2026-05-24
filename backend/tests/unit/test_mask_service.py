import pytest
import numpy as np
from app.business_logic.mask_service import MaskService


def test_apply_mask_zeros_background():
    image = np.ones((4, 4, 4), dtype=np.uint8) * 255
    mask = np.array([
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ], dtype=np.uint8)
    result = MaskService.apply(image, mask)

    assert result[0, 0, 3] == 255  # foreground
    assert result[0, 1, 3] == 0    # background


def test_combine_masks_union():
    m1 = np.array([[1, 0], [0, 0]], dtype=np.uint8)
    m2 = np.array([[0, 1], [0, 0]], dtype=np.uint8)
    combined = MaskService.combine([m1, m2])
    assert combined[0, 0] == True
    assert combined[0, 1] == True
    assert combined[1, 0] == False


def test_apply_preserves_shape():
    image = np.random.randint(0, 255, (100, 100, 4), dtype=np.uint8)
    mask = np.ones((100, 100), dtype=np.uint8)
    result = MaskService.apply(image, mask)
    assert result.shape == (100, 100, 4)