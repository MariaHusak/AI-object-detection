from app.business_logic.color_service import ColorService


def test_random_color_has_4_channels():
    cs = ColorService()
    color = cs.random()
    assert len(color) == 4


def test_random_color_alpha_is_255():
    cs = ColorService()
    color = cs.random()
    assert color[3] == 255


def test_default_color_is_green():
    cs = ColorService()
    color = cs.default()
    assert color == (0, 255, 0, 255)


def test_random_color_in_valid_range():
    cs = ColorService()
    for _ in range(10):
        r, g, b, a = cs.random()
        assert 50 <= r <= 255
        assert 50 <= g <= 255
        assert 50 <= b <= 255