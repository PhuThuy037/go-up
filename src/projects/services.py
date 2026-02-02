from sqlmodel import Session, select

from src.projects.model import Project
from src.projects.schemas import ProjectCreate

def create_project(*, session: Session,project: ProjectCreate , owner_id: int) -> Project:
    project_db = Project.model_validate(project, update={"owner_id": owner_id})
    session.add(project_db)
    session.commit()
    session.refresh(project_db)
    return project_db

def get_all_projects(session: Session) -> list[Project]:
    return list(session.exec(select(Project)).all())

def get_project_by_id(*, session: Session, project_id: int) -> Project:
    stmt = select(Project).where(Project.id == project_id)
    return session.exec(stmt)

def get_project_by_username(*, session: Session, owner_id: int) -> Project:
    stmt = select(Project).where(Project.owner_id == owner_id)
    return session.exec(stmt)


