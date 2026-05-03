from fastapi import APIRouter, UploadFile, File, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.utils.file_validator import validate_image
from app.utils.file_manager import save_upload_file
from app.facades.ai_facade import AIFacade
from app.core.database import get_db

router = APIRouter(prefix="/image", tags=["Image"])


def get_facade(db: Session = Depends(get_db)) -> AIFacade:
    return AIFacade(db)


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
        "detections": facade.detect(path, user_id=user)
    }


@router.post("/detect-preview")
async def detect_preview(
    user=Depends(get_current_user),
    path: str = Depends(save_validated_image),
    facade: AIFacade = Depends(get_facade)
):
    return facade.detect_preview(path, user_id=user)


@router.post("/segment-preview")
async def segment_preview(
    user=Depends(get_current_user),
    path: str = Depends(save_validated_image),
    facade: AIFacade = Depends(get_facade)
):
    return facade.segment_preview(path, user_id=user)


@router.post("/cutout")
async def cutout(
    user=Depends(get_current_user),
    path: str = Depends(save_validated_image),
    facade: AIFacade = Depends(get_facade),
    selected_indices: Optional[List[int]] = Query(default=None),
    mode: str = "multi"
):
    return facade.cutout(path, selected_indices, mode, user_id=user)


@router.post("/replace-background")
async def replace_background(
    user=Depends(get_current_user),
    facade: AIFacade = Depends(get_facade),
    cutout_file: UploadFile = File(...),
    bg_file: UploadFile = File(...)
):
    validate_image(cutout_file)
    image_path = save_upload_file(cutout_file)

    validate_image(bg_file)
    bg_path = save_upload_file(bg_file)

    return facade.replace_background(image_path, bg_path)