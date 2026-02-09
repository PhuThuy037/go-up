from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import Session, select

from src.common.errors import AppError
from src.project_members.model import ProjectMember
from src.tasks.model import Task
from src.tasks.schemas import TaskCreate, TaskPublic, TaskUpdate, TaskUpdateMember
from src.tasks.utils import (
    assert_can_manage_members,
)


def check_task_exist(*, session: Session, task_id) -> Task:
    task_exits = session.get(Task, task_id)
    if not task_exits:
        raise AppError(
            status_code=404,
            code="TASK_NOT_FOUND",
            message="Task not found",
            details=[{"field": "task_id", "reason": "not_found"}],
        )
    return task_exits


def check_task_owner_and_members(
    *,
    session: Session,
    current_id: int,
    project_id: int,
) -> None:
    assert_can_manage_members(
        session=session, project_id=project_id, current_user_id=current_id
    )


def check_member_exits(*, session: Session, project_id: int, user_id: int) -> None:
    stmt = (
        select(ProjectMember)
        .where(ProjectMember.user_id == user_id)
        .where(ProjectMember.project_id == project_id)
    )
    member_project_exist = session.exec(stmt).first()
    if not member_project_exist:
        raise AppError(
            403,
            "FORBIDDEN",
            "Only member in project can add task",
            details=[{"field": "owner_id", "reason": "not_owner"}],
        )


# TODO : Check role: OWNER/LEADER mới được tạo
# TODO : Validate assignee_id (nếu có): phải là member của project (optional nhưng nên làm)
def creat_task(
    *, session: Session, task: TaskCreate, current_id: int, project_id: int
) -> Task:
    check_task_owner_and_members(
        session=session,
        current_id=current_id,
        project_id=project_id,
    )
    task_db = Task.model_validate(task, update={"project_id": project_id})
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    task_db = session.exec(
        select(Task)
        .where(Task.id == task_db.id)
        .options(selectinload(Task.assignee), selectinload(Task.project))
    ).one()
    return task_db


def get_task(*, session: Session, current_user_id: int) -> list[TaskPublic]:
    stmt = (
        select(Task)
        .where(Task.assignee_id == current_user_id)
        .options(joinedload(Task.assignee))
        .options(joinedload(Task.project))
    )
    task = session.exec(stmt).all()
    return task


def update_task(
    *, session: Session, task: TaskUpdate, current_user_id: int, task_id: int
) -> Task:
    assert_can_manage_members(
        session=session, project_id=task.project_id, current_user_id=current_user_id
    )
    task_exist = check_task_exist(session=session, task_id=task_id)
    task_data = task.model_dump(exclude_unset=True)
    task_exist.sqlmodel_update(task_data)
    session.add(task_exist)
    session.commit()
    session.refresh(task_exist)
    return task_exist


def update_task_member(
    *, session: Session, task: TaskUpdateMember, current_user_id: int
) -> Task:
    check_member_exits(
        session=session, project_id=task.project_id, user_id=current_user_id
    )
    task_exist = check_task_exist(session=session, task_id=task.id)
    task_exist.status = task.status
    session.add(task_exist)
    session.commit()
    session.refresh(task_exist)
    return task_exist


# TODO : Check role: OWNER/LEADER mới được tạo
# TODO : Validate assignee_id (nếu có): phải là member của project (optional nhưng nên làm)
def delete_task(
    *, session: Session, project_id: int, task_id: int, current_user_id: int
) -> TaskPublic:
    assert_can_manage_members(
        session=session, project_id=project_id, current_user_id=current_user_id
    )
    task_exist = check_task_exist(session=session, task_id=task_id)
    session.delete(task_exist)
    session.commit()
    session.refresh(task_exist)
    return task_exist
