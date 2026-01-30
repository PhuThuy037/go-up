from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.schemas import *
import src.auth.service as user_service
from fastapi import APIRouter, Depends
from src.deps import SessionDep
from src.auth.deps import CurrentUser

router = APIRouter(prefix="/user", tags=["user"])

@router.post("", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    return user_service.create_user(user=user, session =session)

@router.get("", response_model=list[UserPublic])
def get_all_users(session: SessionDep):
    return user_service.get_all_users(session=session)

@router.get("/username/{username}", response_model=UserPublic)
def get_user_by_username(session: SessionDep, username: str):
    return user_service.get_user_by_username(session=session, username=username)

@router.get("/me", response_model=UserPublic)
def get_me(current_user : CurrentUser):
    return current_user

@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id : int, user: UserUpdate, session: SessionDep):
    return user_service.update_user(user_id=user_id, user=user, session=session)

@router.delete("/{user_id}", response_model=UserPublic)
def delete_user(user_id : int, session: SessionDep):
    return user_service.delete_user_by_user_id(session=session, user_id=user_id)

@router.post("/login")
def login_user(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
):
    return user_service.login(session=session, email=form.username, password=form.password)
