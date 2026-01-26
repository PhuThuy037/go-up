from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from src.auth.user_role import UserRole
from src.util.util import utc_now
from src.project_members.model import ProjectMember

if TYPE_CHECKING:
    from src.projects.model import Project
    from src.comments.model import Comment
    from src.tasks.model import Task

class User(SQLModel, table=True):
    __tablename__ = "users"
    username: str = Field(min_length=1, max_length=30)
    email: EmailStr = Field(min_length=1, max_length=30, unique=True)
    role: UserRole = Field(default=UserRole.USER)
    id: Optional[int] = Field(default=None, primary_key=True)
    projects: list["Project"] = Relationship(back_populates="members", link_model=ProjectMember)
    comments: list["Comment"] = Relationship(back_populates="user")
    assigned_tasks: list["Task"] = Relationship(back_populates="assignee")
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
