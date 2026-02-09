from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class CommentBase(SQLModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentPublic(CommentBase):
    id: Optional[int]
    created_at: datetime
    user_id: int


@dataclass(frozen=True)
class CommentCtx:
    current_user_id: int
    task_id: int
