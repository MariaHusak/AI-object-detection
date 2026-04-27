from fastapi import APIRouter, Depends
from app.schemas.auth_schema import *
from app.factories.auth_factory import AuthFactory
from app.core.database import get_db

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(data: RegisterRequest, db=Depends(get_db)):
    auth = AuthFactory.create(db)

    return auth.register(
        data.username,
        data.password
    )


@router.post("/login")
def login(data: LoginRequest, db=Depends(get_db)):
    auth = AuthFactory.create(db)

    return auth.login(
        data.username,
        data.password
    )

