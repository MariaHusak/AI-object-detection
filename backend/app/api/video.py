from fastapi import APIRouter, UploadFile, File

from app.utils.file_manager import save_upload_file
from app.facades.ai_facade import AIFacade

router = APIRouter(prefix="/video", tags=["Video"])

facade = AIFacade()


@router.get("/")
def video_home():
    return {
        "message": "Video API ready"
    }


@router.post("/process")
async def process_video(file: UploadFile = File(...)):
    path = save_upload_file(file)
    return facade.process_video(path)


@router.post("/process-async")
async def process_video(file: UploadFile = File(...)):
    path = save_upload_file(file)
    return facade.process_video_async(path)


@router.get("/status/{task_id}")
async def get_status(task_id: str):
    return facade.get_task_status(task_id)


