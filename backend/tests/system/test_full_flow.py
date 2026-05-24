import pytest
import io
from unittest.mock import patch, MagicMock
from PIL import Image
import numpy as np


def _make_image_bytes():
    img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def _register_and_login(client, username="sysuser"):
    client.post("/auth/register", json={"username": username, "password": "pass123"})
    resp = client.post("/auth/login", json={"username": username, "password": "pass123"})
    return resp.json()["access_token"]


@patch("app.facades.ai_facade.PipelineFactory")
@patch("app.facades.ai_facade.DrawService")
@patch("app.facades.ai_facade.VideoService")
@patch("app.facades.ai_facade.CutoutService")
@patch("app.facades.ai_facade.BackgroundService")
@patch("app.utils.file_validator.validate_image")
@patch("app.utils.file_manager.save_upload_file")
def test_full_register_login_detect_stats(
    mock_save, mock_validate,
    MockBg, MockCutout, MockVideo, MockDraw, MockPipeline,
    client
):
    mock_save.return_value = "uploads/test.png"
    pipeline_instance = MagicMock()
    pipeline_instance.detector.detect.return_value = [
        {"class": "person", "confidence": 0.92, "box": [10, 10, 80, 80]}
    ]
    MockPipeline.create.return_value = pipeline_instance

    draw_instance = MagicMock()
    draw_instance.draw_boxes.return_value = "http://localhost:8000/outputs/x.png"
    draw_instance._to_public_url.return_value = "http://localhost:8000/outputs/x.png"
    MockDraw.return_value = draw_instance

    # Реєстрація
    reg = client.post("/auth/register", json={"username": "flowuser", "password": "pass"})
    assert reg.status_code == 200

    # Логін
    login = client.post("/auth/login", json={"username": "flowuser", "password": "pass"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Детекція
    img_bytes = _make_image_bytes()
    detect_resp = client.post(
        "/image/detect",
        files={"file": ("test.png", img_bytes, "image/png")},
        headers=headers
    )
    assert detect_resp.status_code == 200
    assert "detections" in detect_resp.json()

    # Перевірка статистики
    stats_resp = client.get("/stats/", headers=headers)
    assert stats_resp.status_code == 200
    assert stats_resp.json()["processed"] >= 1