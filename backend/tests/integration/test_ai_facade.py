import pytest
from unittest.mock import MagicMock, patch
from app.facades.ai_facade import AIFacade
from app.models.user import User
from app.repositories.processing_repository import ProcessingRepository

@pytest.fixture
def facade(db):
    with patch("app.facades.ai_facade.PipelineFactory") as MockFactory, \
         patch("app.facades.ai_facade.DrawService") as MockDraw, \
         patch("app.facades.ai_facade.CutoutService") as MockCutout, \
         patch("app.facades.ai_facade.BackgroundService") as MockBg, \
         patch("app.facades.ai_facade.VideoService") as MockVideo:

        f = AIFacade(db)
        f.pipeline = MagicMock()
        f.drawer = MagicMock()
        f.cutter = MagicMock()
        f.bg_service = MagicMock()
        f.video_service = MagicMock()
        yield f


def test_detect_returns_detections(facade, db):
    fake_dets = [{"class": "cat", "confidence": 0.95, "box": [0, 0, 100, 100]}]
    facade.pipeline.detector.detect.return_value = fake_dets

    result = facade.detect("fake/path.jpg")
    assert result == fake_dets


def test_detect_saves_log_for_user(facade, db):
    user = User(username="testuser", password="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)

    fake_dets = [{"class": "dog", "confidence": 0.8, "box": [10, 10, 50, 50]}]
    facade.pipeline.detector.detect.return_value = fake_dets

    facade.detect("fake/path.jpg", user_id=user.id)

    stats = ProcessingRepository(db).get_user_stats(user.id)
    assert stats["processed"] == 1


def test_filter_detections_by_indices(facade, db):
    dets = [
        {"class": "cat", "confidence": 0.9, "box": [0, 0, 10, 10]},
        {"class": "dog", "confidence": 0.8, "box": [5, 5, 15, 15]},
    ]
    facade.pipeline.detector.detect.return_value = dets
    facade.pipeline.segmenter.segment.return_value = [MagicMock()]

    facade.drawer.draw_segmentation.return_value = "url"
    facade._detect_and_segment("path.jpg", selected_indices=[0])

    called_dets = facade.pipeline.segmenter.segment.call_args[0][1]
    assert len(called_dets) == 1
    assert called_dets[0]["class"] == "cat"


def test_replace_background_returns_url(facade, db):
    facade.bg_service.replace_background.return_value = "outputs/result.png"
    result = facade.replace_background("img.png", "bg.png")
    assert "result_image" in result