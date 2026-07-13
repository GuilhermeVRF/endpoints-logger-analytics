from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core import security
from core import schemas
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: schemas.UserCreate):
        existing_user = self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de usuário já registrado.",
            )

        hashed_password = security.get_password_hash(user_data.password)
        return self.user_repository.create(
            username=user_data.username,
            password=hashed_password,
            role=user_data.role,
        )

    def login_user(self, form_data: OAuth2PasswordRequestForm):
        user = self.user_repository.get_by_username(form_data.username)
        if not user or not security.verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nome de usuário ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = security.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
