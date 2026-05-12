import os

from celery import Celery

broker = os.getenv(
    "REDIS_BROKER_URL",
    "redis://localhost:6379/0"
)

backend = os.getenv(
    "REDIS_BACKEND_URL",
    "redis://localhost:6379/1"
)

celery_app = Celery(
    "ai_tasks",
    broker=broker,
    backend=backend
)

celery_app.conf.task_track_started = True

import app.workers.celery_tasks