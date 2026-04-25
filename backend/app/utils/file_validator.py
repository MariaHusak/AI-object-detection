from fastapi import HTTPException, UploadFile


IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg"
}

VIDEO_TYPES = {
    "video/mp4",
    "video/x-msvideo",
    "video/quicktime",
    "video/x-matroska",
}


def validate_image(file: UploadFile):
    if file.content_type not in IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed (jpg, jpeg, png, webp)"
        )


def validate_video(file: UploadFile):
    if file.content_type not in VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only video files are allowed (mp4, avi, mov, mkv)"
        )
