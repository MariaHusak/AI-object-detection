from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.repositories.processing_repository import ProcessingRepository
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/")
def get_stats(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = ProcessingRepository(db)
    return repo.get_user_stats(user)