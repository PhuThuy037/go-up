from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from src.auth.schemas import UserPublic


class ProjectBase(SQLModel):
    title: str
    description: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: Optional[str] = Field(default=None, min_length=3, max_length=300)
    description: Optional[str] = Field(default=None)


class ProjectPublic(ProjectBase):
    id: int
    title: str
    description: Optional[str]
    owner_id: int
    owner: UserPublic
    model_config = ConfigDict(from_attributes=True)
