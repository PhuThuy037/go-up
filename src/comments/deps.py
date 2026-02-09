from typing import Annotated

from fastapi import Depends

from src.auth.deps import CurrentUser
from src.comments.schemas import CommentCtx


def get_comment_ctx(task_id: int, curent_user: CurrentUser):
    return CommentCtx(task_id=task_id, current_user_id=curent_user.id)


CommentCtxDeps = Annotated[CommentCtx, Depends(get_comment_ctx)]
