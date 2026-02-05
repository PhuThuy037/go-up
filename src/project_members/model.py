from datetime import datetime, timezone
from src.util.util import utc_now
from sqlmodel import SQLModel, Field, Relationship
from src.project_members.project_role import ProjectRole

class ProjectMember(SQLModel, table=True):
    __tablename__ = "project_members"
    project_id: int = Field(foreign_key="projects.id",primary_key=True)
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role: ProjectRole = Field(default=ProjectRole.MEMBER)
    joined_at: datetime = Field(default_factory=utc_now)