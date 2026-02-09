from fastapi import APIRouter
from src.deps import SessionDep
from src.auth.deps import CurrentUser
import src.project_members.servies as services
from src.project_members.deps import MemberCtxDeps, AddMemberBody

from src.project_members.schemas import ProjectMemberPublic, ProjectMemberUpdate

router = APIRouter(prefix="/projects_member", tags=["projects_member"])

@router.get("/{project_id}/members")
def get_project_members(project_id: int, session: SessionDep, current_user: CurrentUser):
    return services.list_members(session=session, project_id=project_id, current_user_id=current_user.id)

@router.post("/{project_id}/members", response_model=ProjectMemberPublic)
def add_member(session: SessionDep,project_id: int ,body: AddMemberBody, current_user: CurrentUser):
    return services.add_member(
        session=session,
        project_id=project_id,
        current_user_id=current_user.id,
        user_id=body.user_id,
        role=body.role,
    )

@router.patch("/{project_id}/members/{user_id}", response_model=ProjectMemberPublic)
def update_member_role(session: SessionDep,ctx:  MemberCtxDeps , role: ProjectMemberUpdate):
    return services.update_member_role(
        session=session,
        ctx=ctx,
        role=role.role
    )

@router.delete("/{project_id}/members/{user_id}")
def delete_member_role(session: SessionDep, ctx: MemberCtxDeps):
    return services.remove_member(session=session, ctx=ctx)

