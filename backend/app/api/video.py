from fastapi import APIRouter, UploadFile, File, Depends

from app.utils.file_validator import validate_video
from app.utils.file_manager import save_upload_file
from app.facades.ai_facade import AIFacade

router = APIRouter(prefix="/video", tags=["Video"])


def get_facade() -> AIFacade:
    return AIFacade()


def save_validated_video(file: UploadFile = File(...)) -> str:
    validate_video(file)
    return save_upload_file(file)


@router.get("/")
def video_home():
    return {"message": "Video API ready"}


@router.post("/process")
async def process_video(
    path: str = Depends(save_validated_video),
    facade: AIFacade = Depends(get_facade)
):
    return facade.process_video(path)


@router.post("/process-async")
async def process_video_async(
    path: str = Depends(save_validated_video),
    facade: AIFacade = Depends(get_facade)
):
    return facade.process_video_async(path)


@router.get("/status/{task_id}")
async def get_task_status(
    task_id: str,
    facade: AIFacade = Depends(get_facade)
):
    return facade.get_task_status(task_id)