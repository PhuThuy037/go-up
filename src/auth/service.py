from fastapi import HTTPException

from src.auth.security import hash_password, verify_password, generate_jwt_token, verify_jwt_token
from src.auth.schemas import UserCreate, UserUpdate
from src.auth.model import User
from sqlmodel import Session
from sqlmodel import  select

def create_user(*, session: Session, user: UserCreate) -> User:
    stmt = select(User).where(User.email == user.email)
    user_exist = session.exec(stmt).first()
    hashed_pw = hash_password(user.password)
    if user_exist:
        raise HTTPException(status_code=409, detail="Email already registered")
    user_db = User.model_validate(user, update={"password_hash": hashed_pw})
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

def get_all_users(session: Session) -> list[User]:
    return list(session.exec(select(User)).all())

def get_user_by_username(session: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return session.exec(stmt).first()

def get_user_by_id(*, session: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return session.exec(stmt).first()

def delete_user_by_user_id(*, session: Session, user_id: int) -> dict:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

def update_user(user_id: int, user: UserUpdate, session: Session) -> User:
    user_exist = session.get(User, user_id)
    if not user_exist:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)

    if "password" in user_data:
        plain_password = user_data.pop("password")
        user_exist.password_hash = hash_password(plain_password)
    user_exist.sqlmodel_update(user_data)
    session.add(user_exist)
    session.commit()
    session.refresh(user_exist)
    return user_exist

def authenticate_user(*, session: Session, email: str, password: str) -> User:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def login(*, session: Session, email: str, password: str) -> dict:
    user = authenticate_user(session=session, email=email, password=password)
    token = generate_jwt_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

def get_user_from_token(*, session: Session, token: str) -> User:
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Missing sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalid")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


