from fastapi import APIRouter, UploadFile, File, Query, Depends
from typing import List, Optional
from app.auth.dependencies import get_current_user
from app.utils.file_validator import validate_image
from app.utils.file_manager import save_upload_file
from app.facades.ai_facade import AIFacade

router = APIRouter(prefix="/image", tags=["Image"])


def get_facade() -> AIFacade:
    return AIFacade()


def save_validated_image(file: UploadFile = File(...)) -> str:
    validate_image(file)
    return save_upload_file(file)


@router.get("/")
def image_home():
    return {"message": "Image API ready"}


@router.post("/detect")
async def detect(
    user=Depends(get_current_user),
    path: str = Depends(save_validated_image),
    facade: AIFacade = Depends(get_facade)
):
    return {
        "file": path,
        "detections": facade.detect(path)
    }


@router.post("/detect-preview")
async def detect_preview(
    user=Depends(get_current_user),
    path: str = Depends(save_validated_image),
    facade: AIFacade = Depends(get_facade)
):
    return facade.detect_preview(path)


@router.post("/segment-preview")
async def segment_preview(
    user=Depends(get_current_user),
    path: str = Depends(save_validated_image),
    facade: AIFacade = Depends(get_facade)
):
    return facade.segment_preview(path)


@router.post("/cutout")
async def cutout(
    user=Depends(get_current_user),
    path: str = Depends(save_validated_image),
    facade: AIFacade = Depends(get_facade),
    selected_indices: Optional[List[int]] = Query(default=None),
    mode: str = "multi"
):
    return facade.cutout(path, selected_indices, mode)


@router.post("/replace-background")
async def replace_background(
    user=Depends(get_current_user),
    facade: AIFacade = Depends(get_facade),
    image_path: str = Depends(save_validated_image),
    bg_file: UploadFile = File(...),
    selected_indices: Optional[List[int]] = Query(default=None)
):
    bg_path = save_upload_file(bg_file)
    validate_image(bg_file)
    return facade.replace_background(image_path, bg_path, selected_indices)