from fastapi import APIRouter
import src.projects.services as project_services
import src.projects.schemas as project_schema
from src.deps import SessionDep
from src.auth.deps import CurrentUser
router = APIRouter(prefix="/projects", tags=["project"])

@router.post("", response_model=project_schema.ProjectPublic)
def create_new_project(session: SessionDep,project: project_schema.ProjectCreate ,current_user: CurrentUser):
    return project_services.create_project(session=session,project=project, owner_id=current_user.id)

@router.get("/", response_model=list[project_schema.ProjectPublic])
def get_all_project(session: SessionDep):
    return project_services.get_all_projects(session)

@router.get("/{project_id}", response_model=project_schema.ProjectPublic)
def get_project_by_id(project_id: int, session: SessionDep):
    return project_services.get_project_by_id(session=session, project_id=project_id)

@router.get("/{user_id}", response_model=project_schema.ProjectPublic)
def get_project_by_username(user_id: int, session: SessionDep):
    return project_services.get_project_by_username(session=session, owner_id=user_id)

@router.patch("/{project_id}", response_model=project_schema.ProjectPublic)
def update_project(*, session: SessionDep, project_id: int, project: project_schema.ProjectUpdate,current_user: CurrentUser):
    return project_services.update_project(session=session, project_id=project_id, project=project, current_user_id=current_user.id)