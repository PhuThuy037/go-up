
from sqlmodel import Session, select

from src.common.errors import AppError
from src.project_members.deps import MemberCtx
from src.project_members.model import ProjectMember
from src.project_members.project_role import ProjectRole
from src.project_members.schemas import ProjectMemberCreate , ProjectMemberBase
from src.projects.model import Project
from src.auth.model import User


def check_project_exists(*, session ,project_id: int) -> Project:
    project_exist = session.get(Project, project_id)
    if not project_exist:
        raise AppError(
            status_code=404,
            code="PROJECT_NOT_FOUND",
            message="Project not found",
            details=[{"field": "project_id", "reason": "not_found"}],
        )
    return project_exist

def check_member_exist(*, session ,user_id)-> User:
    member_exist = session.get(User, user_id)
    if not member_exist:
        raise AppError(
            status_code=404,
            code="USER_NOT_FOUND",
            message="User not found",
            details=[{"field": "user_id", "reason": "not_found"}],
        )
    return member_exist

def check_author_project(*, session,project_id: int ,current_user_id) -> None:
    project = check_project_exists(session=session, project_id=project_id)
    if project.owner_id == current_user_id:
        return
    raise AppError(
        status_code=403,
        code="USER_NOT_PERMITTED",
        message="User not permitted",
        details=[{"field": "current_user_id", "reason": "not_permitted"}],
    )


def assert_can_manage_members(*, session, project_id: int ,current_user_id: int) -> None:
    project = check_project_exists(session=session, project_id=project_id)
    if project.owner_id == current_user_id:
        return

    stmt = select(ProjectMember).where(
        ProjectMember.user_id == current_user_id,
        ProjectMember.project_id == project_id,
    )
    project_member = session.execute(stmt).first()

    if project_member.role == ProjectRole.LEADER:
        return

    raise AppError(
        status_code=403,
        code="USER_NOT_PERMITTED",
        message="User not permitted",
        details=[{"field": "current_user_id", "reason": "not_permitted"}],
    )


def add_member(*, session: Session, project_id: int, user_id: int, current_user_id : int, role: ProjectRole ) -> ProjectMember:
    user_exist = check_member_exist(session=session, user_id=user_id)
    assert_can_manage_members(
        session=session,
        project_id=project_id,
        current_user_id=current_user_id
    )
    project_db = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role if role is not None else ProjectRole.MEMBER,
    )
    session.add(project_db)
    session.commit()
    session.refresh(project_db)
    return project_db

def remove_member(*, session, ctx: MemberCtx) -> dict:
    check_author_project(
        session=session,
        project_id=ctx.project_id,
        current_user_id=ctx.current_user_id
    )

    assert_can_manage_members(
        session=session,
        project_id=ctx.project_id,
        current_user_id=ctx.current_user_id
    )
    stmt = select(ProjectMember).where(
        ProjectMember.user_id == ctx.user_id,
        ProjectMember.project_id == ctx.project_id,
    )
    project_db = session.exec(stmt).first()
    session.delete(project_db)
    session.commit()
    return {"ok": True}

def update_member_role(*, session,ctx: MemberCtx ,role: ProjectRole) -> ProjectMember:
    check_author_project(
        session=session,
        project_id=ctx.project_id,
        current_user_id=ctx.current_user_id
    )
    stmt = select(ProjectMember).where(
        ProjectMember.user_id == ctx.user_id,
        ProjectMember.project_id == ctx.project_id,
    )
    project_member = session.exec(stmt).first()
    project_member.role = role
    session.commit()
    session.refresh(project_member)
    return project_member

def list_members(*, session: Session ,project_id: int ,current_user_id: int) -> list[dict]:
    assert_can_manage_members(
        session=session,
        project_id=project_id,
        current_user_id=current_user_id
    )
    stmt = (
        select(
            User.id,
            User.username,
            User.email,
            ProjectMember.role,
            ProjectMember.joined_at,
        )
        .join(ProjectMember, ProjectMember.user_id == User.id)
        .where(ProjectMember.project_id == project_id)
        .order_by(ProjectMember.joined_at.asc())
    )
    rows = session.exec(stmt).all()
    return [
        {
            "user_id": row.id,
            "username": row.username,
            "email": row.email,
            "role": row.role,
            "joined_at": row.joined_at,
        }
        for row in rows
    ]

