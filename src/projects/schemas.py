from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import  ConfigDict

from src.auth.schemas import UserPublic


# class Project(SQLModel, table=True):
#     __tablename__ = "projects"
#
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     description: Optional[str] = None
#     owner_id: int = Field(foreign_key="users.id")  # Người tạo (Owner)
#     owner: "User" = Relationship()
#     # Relationship (để query ngược cho tiện)
#     tasks: list["Task"] = Relationship(back_populates="project")
#     # Link tới Members (Advance)
#     members: list["User"] = Relationship(back_populates="projects", link_model=ProjectMember)

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
    owner_id : int
    owner : UserPublic
    model_config = ConfigDict(from_attributes=True)
