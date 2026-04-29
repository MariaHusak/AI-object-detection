from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.image import router as image_router
from .api.video import router as video_router
from app.api.auth import router as auth_router
from app.core.database import Base, engine
from app.models.user import User
from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Object Detection System",
    version="1.0.0",
    description="Backend for object detection, segmentation and image processing"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router)
app.include_router(video_router)
app.include_router(auth_router)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {
        "message": "Backend is running",
        "status": "success"
    }

