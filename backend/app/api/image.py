from fastapi import APIRouter, UploadFile, File, Query
from typing import List, Optional

from app.utils.file_manager import save_upload_file
from app.facades.ai_facade import AIFacade

router = APIRouter(prefix="/image", tags=["Image"])

facade = AIFacade()



@router.get("/")
def image_home():
    return {"message": "Image API ready"}


@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    path = save_upload_file(file)
    result = facade.detect(path)

    return {
        "file": path,
        "detections": result
    }


@router.post("/detect-preview")
async def detect_preview(file: UploadFile = File(...)):
    path = save_upload_file(file)
    result = facade.detect_preview(path)

    return result


@router.post("/segment-preview")
async def segment_preview(file: UploadFile = File(...)):
    path = save_upload_file(file)
    return facade.segment_preview(path)


@router.post("/cutout")
async def cutout(
    file: UploadFile = File(...),
    selected_indices: Optional[List[int]] = Query(default=None),
    mode: str = "multi"
):
    path = save_upload_file(file)

    return facade.cutout(path, selected_indices, mode)


@router.post("/replace-background")
async def replace_background(
    file: UploadFile = File(...),
    bg_file: UploadFile = File(...),
    selected_indices: Optional[List[int]] = Query(default=None)
):
    image_path = save_upload_file(file)
    bg_path = save_upload_file(bg_file)

    return facade.replace_background(
        image_path,
        bg_path,
        selected_indices
    )


