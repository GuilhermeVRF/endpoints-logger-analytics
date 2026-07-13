from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import schemas
from core.dependencies import get_db
from repositories.user_repository import UserRepository
from services.auth_service import AuthService

router = APIRouter(tags=["auth"])


@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    service = AuthService(UserRepository(db))
    return service.register_user(user)


@router.post("/login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = AuthService(UserRepository(db))
    return service.login_user(form_data)
