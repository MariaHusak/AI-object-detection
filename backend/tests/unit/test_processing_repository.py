from app.repositories.processing_repository import ProcessingRepository
from app.models.user import User


def _create_user(db, username="testuser"):
    user = User(username=username, password="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_create_and_get_stats(db):
    user = _create_user(db)
    repo = ProcessingRepository(db)
    repo.create(user_id=user.id, time=1.5, accuracy=0.9)
    repo.create(user_id=user.id, time=0.5, accuracy=0.8)

    stats = repo.get_user_stats(user_id=user.id)
    assert stats["processed"] == 2
    assert abs(stats["avg_time"] - 1.0) < 0.01
    assert abs(stats["avg_accuracy"] - 0.85) < 0.01


def test_empty_stats(db):
    repo = ProcessingRepository(db)
    stats = repo.get_user_stats(user_id=999)
    assert stats["processed"] == 0
    assert stats["avg_time"] == 0
    assert stats["avg_accuracy"] == 0