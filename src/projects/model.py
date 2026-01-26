from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from src.project_members.model import ProjectMember


if TYPE_CHECKING:
    from src.auth.model import User
    from src.tasks.model import Task

class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="users.id")  # Người tạo (Owner)
    owner: "User" = Relationship()
    # Relationship (để query ngược cho tiện)
    tasks: list["Task"] = Relationship(back_populates="project")
    # Link tới Members (Advance)
    members: list["User"] = Relationship(back_populates="projects", link_model=ProjectMember)