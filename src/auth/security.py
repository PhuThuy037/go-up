import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from src.config import settings


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def generate_jwt_token(user_id: str | int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.auth_jwt_secret_expiration))
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.auth_jwt_secret, algorithm=settings.auth_jwt_algorithm)

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.auth_jwt_secret, algorithms=[settings.auth_jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )