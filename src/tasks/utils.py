from sqlmodel import select

from src.auth.model import User
from src.common.errors import AppError
from src.project_members.model import ProjectMember
from src.project_members.project_role import ProjectRole
from src.projects.model import Project


def check_project_exists(*, session, project_id: int) -> Project:
    project_exist = session.get(Project, project_id)
    if not project_exist:
        raise AppError(
            status_code=404,
            code="PROJECT_NOT_FOUND",
            message="Project not found",
            details=[{"field": "project_id", "reason": "not_found"}],
        )
    return project_exist


def check_member_exist(*, session, user_id) -> User:
    member_exist = session.get(User, user_id)
    if not member_exist:
        raise AppError(
            status_code=404,
            code="USER_NOT_FOUND",
            message="User not found",
            details=[{"field": "user_id", "reason": "not_found"}],
        )
    return member_exist


def check_author_project(*, session, project_id: int, current_user_id) -> None:
    project = check_project_exists(session=session, project_id=project_id)
    if project.owner_id == current_user_id:
        return
    raise AppError(
        status_code=403,
        code="USER_NOT_PERMITTED",
        message="User not permitted",
        details=[{"field": "current_user_id", "reason": "not_permitted"}],
    )


def assert_can_manage_members(
    *, session, project_id: int, current_user_id: int
) -> None:
    project = check_project_exists(session=session, project_id=project_id)
    if project.owner_id == current_user_id:
        return

    stmt = select(ProjectMember).where(
        ProjectMember.user_id == current_user_id,
        ProjectMember.project_id == project_id,
    )
    project_member = session.exec(stmt).first()

    if project_member.role == ProjectRole.LEADER:
        return

    raise AppError(
        status_code=403,
        code="USER_NOT_PERMITTED",
        message="User not permitted",
        details=[{"field": "current_user_id", "reason": "not_permitted"}],
    )
