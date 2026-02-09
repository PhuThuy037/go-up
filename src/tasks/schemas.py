from typing import Optional

from sqlmodel import Field, SQLModel

from src.auth.schemas import UserPublic
from src.projects.schemas import ProjectPublic
from src.tasks.task_status import TaskStatus


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.todo)


class TaskCreate(TaskBase):
    assignee_id: int


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None


class TaskUpdateMember(SQLModel):
    status: TaskStatus


class TaskPublic(TaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    project: Optional[ProjectPublic] = None
    assignee: Optional[UserPublic] = None
