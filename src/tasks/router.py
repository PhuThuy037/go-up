from fastapi import APIRouter

import src.tasks.services as services
from src.auth.deps import CurrentUser
from src.deps import SessionDep
from src.tasks.schemas import TaskCreate, TaskPublic, TaskUpdate

router = APIRouter(prefix="/project/{project_id}/task", tags=["tasks"])


@router.get("", response_model=list[TaskPublic])
def get_tasks(current_user: CurrentUser, session: SessionDep):
    return services.get_task(session=session, current_user_id=current_user.id)


@router.post("", response_model=TaskPublic)
def create_task(
    session: SessionDep, task: TaskCreate, current_user: CurrentUser, project_id: int
):
    return services.creat_task(
        session=session, task=task, current_id=current_user.id, project_id=project_id
    )


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: int, current_user: CurrentUser, session: SessionDep, task: TaskUpdate
):
    return services.update_task(
        session=session, task=task, current_user_id=current_user.id, task_id=task_id
    )


@router.delete("/{task_id}")
def delete_task(
    session: SessionDep, task_id: int, current_user: CurrentUser, project_id: int
):
    return services.delete_task(
        session=session,
        task_id=task_id,
        current_user_id=current_user.id,
        project_id=project_id,
    )
