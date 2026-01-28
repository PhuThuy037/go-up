from datetime import datetime

from sqlmodel import SQLModel, Field
from pydantic import EmailStr, ConfigDict
from typing import Optional

class UserBase(SQLModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = Field(default=None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6)

class UserLogin(UserBase):
    email: EmailStr
    password: str

class UserPublic(UserBase):
    id: int
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)