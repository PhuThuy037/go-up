from typing import Type

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.comments.model import Comment
from src.comments.schemas import CommentCreate, CommentCtx, CommentUpdate
from src.common.errors import AppError
from src.tasks.services import check_task_exist


def check_comment_exist(*, session: Session, comment_id: int) -> Type[Comment]:
    comment_db = session.get(Comment, comment_id)
    if not comment_db:
        raise AppError(
            404,
            "NOT_FOUND",
            "Cannot find comment with id {}".format(comment_id),
            details=[{"field": "comment_id", "reason": "not_found"}],
        )
    return comment_db


def create_comment(
    *, session: Session, comment: CommentCreate, ctx: CommentCtx
) -> Comment:
    check_task_exist(session=session, task_id=ctx.task_id)
    comment_db = Comment.model_validate(
        comment, update={"task_id": ctx.task_id, "user_id": ctx.current_user_id}
    )
    session.add(comment_db)
    session.commit()
    session.refresh(comment_db)
    return comment_db


def get_comment_by_user_id(*, session: Session, current_user_id: int) -> list[Comment]:
    return session.exec(
        select(Comment)
        .where(Comment.user_id == current_user_id)
        .options(selectinload(Comment.task))
    ).all()


def update_comment(
    *, session: Session, current_user_id: int, comment_id: int, comment: CommentUpdate
) -> Comment:
    comment_exist = check_comment_exist(session=session, comment_id=comment_id)
    if comment_exist.user_id != current_user_id:
        raise AppError(
            403,
            "PERMISSION_DENIED",
            "You must be ower comment",
            details=[{"field": "comment_id", "reason": "not_owner"}],
        )
    comment_exist.content = comment.content
    session.commit()
    session.refresh(comment_exist)
    return comment_exist


def delete_comment(*, session: Session, comment_id: int, current_user_id) -> dict:
    comment_exist = check_comment_exist(session=session, comment_id=comment_id)
    if comment_exist.user_id != current_user_id:
        raise AppError(
            403,
            "PERMISSION_DENIED",
            "You must be ower comment",
            details=[{"field": "comment_id", "reason": "not_owner"}],
        )
    session.delete(comment_exist)
    session.commit()
    return {"ọk": True}
