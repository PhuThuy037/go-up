from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from src.projects.model import Project
from src.comments.model import Comment
from src.tasks.task_status import TaskStatus
if TYPE_CHECKING:
    from src.projects.model import Project
    from src.auth.model import User
    from src.comments.model import Comment


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: str = Field(default="Todo")  # Todo, Doing, Done

    project_id: int = Field(foreign_key="projects.id")
    assignee_id: Optional[int] = Field(foreign_key="users.id", default=None)  # Có thể chưa gán cho ai
    assignee: Optional["User"] = Relationship(back_populates="assigned_tasks")
    # Relationship
    project: "Project" = Relationship(back_populates="tasks")
    comments: list[Comment] = Relationship(back_populates="task")
