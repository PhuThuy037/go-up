from fastapi import APIRouter

import src.comments.services as comments_services
from src.auth.deps import CurrentUser
from src.comments.deps import CommentCtxDeps
from src.comments.response import CommentWithTask
from src.comments.schemas import CommentCreate, CommentPublic, CommentUpdate
from src.deps import SessionDep

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/task/{task_id}", response_model=CommentPublic)
def create_comment(
    task_id: int,
    comment: CommentCreate,
    session: SessionDep,
    ctx: CommentCtxDeps,
):
    return comments_services.create_comment(session=session, comment=comment, ctx=ctx)


@router.get("", response_model=list[CommentWithTask])
def get_comment(session: SessionDep, current_user: CurrentUser):
    return comments_services.get_comment_by_user_id(
        session=session, current_user_id=current_user.id
    )


@router.patch("{comment_id}", response_model=CommentPublic)
def update_comment(
    session: SessionDep,
    comment_id: int,
    comment: CommentUpdate,
    current_user: CurrentUser,
):
    return comments_services.update_comment(
        comment_id=comment_id,
        comment=comment,
        session=session,
        current_user_id=current_user.id,
    )


@router.delete("/{comment_id}")
def delete_comment(session: SessionDep, comment_id: int, current_user: CurrentUser):
    return comments_services.delete_comment(
        session=session, comment_id=comment_id, current_user_id=current_user.id
    )
