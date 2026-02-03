from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from src.common.errors import AppError
from src.projects.model import Project
from src.projects.schemas import ProjectCreate, ProjectUpdate


def create_project(*, session: Session,project: ProjectCreate , owner_id: int) -> Project:
    project_db = Project.model_validate(project, update={"owner_id": owner_id})
    session.add(project_db)
    session.commit()
    session.refresh(project_db)
    return project_db

def get_all_projects(session: Session) -> list[Project]:
    return list(session.exec(select(Project)).all())

def get_project_by_id(*, session: Session, project_id: int) -> Project:
    stmt = select(Project).where(Project.id == project_id).options(joinedload(Project.owner))
    project =  session.exec(stmt).first()
    if not project:
         raise AppError(
            status_code=404,
            code="PROJECT_NOT_FOUND",
            message="Project not found",
            details=[{"field": "project_id", "reason": "not_found"}],
        )
    return project

def get_project_by_username(*, session: Session, owner_id: int) -> Project:
    stmt = select(Project).where(Project.owner_id == owner_id).options(joinedload(Project.owner))
    return session.exec(stmt).all()

def update_project(*, session: Session,project_id: int ,project: ProjectUpdate,current_user_id: int) -> Project:
    project_exist = session.get(Project, project_id)
    if not project_exist:
        raise AppError(
            status_code=404,
            code="PROJECT_NOT_FOUND",
            message="Project not found",
            details=[{"field": "project_id", "reason": "not_found"}],
        )
    if project_exist.owner_id != current_user_id:
        raise AppError(403, "FORBIDDEN", "Only owner can update this project",
                       details=[{"field": "owner_id", "reason": "not_owner"}])
    project_exist.sqlmodel_update(project)
    session.commit()
    session.refresh(project_exist)
    return project_exist
