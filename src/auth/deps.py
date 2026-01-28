from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from src.deps import SessionDep
from src.auth.model import User
from src.auth import service as auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
) -> User:
    return auth_service.get_user_from_token(session=session, token=token)

CurrentUser = Annotated[User, Depends(get_current_user)]
