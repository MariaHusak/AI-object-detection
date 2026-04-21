from celery import Celery

celery_app = Celery(
    "ai_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery_app.conf.task_track_started = True

import app.workers.celery_tasks
