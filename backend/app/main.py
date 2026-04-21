from fastapi import FastAPI
from .api.image import router as image_router
from .api.video import router as video_router

app = FastAPI(
    title="AI Object Detection System",
    version="1.0.0",
    description="Backend for object detection, segmentation and image processing"
)

app.include_router(image_router)
app.include_router(video_router)


@app.get("/")
def home():
    return {
        "message": "Backend is running",
        "status": "success"
    }

