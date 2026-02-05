from sqlmodel import SQLModel
from datetime import datetime
from src.project_members.project_role import ProjectRole


class ProjectMemberBase(SQLModel):
    project_id: int
    user_id: int

class ProjectMemberCreate(ProjectMemberBase):
    pass
class ProjectMemberUpdate(SQLModel):
    role: ProjectRole

class ProjectMemberPublic(ProjectMemberBase):
    role: ProjectRole
    joined_at: datetime