from typing import Optional

from src.comments.schemas import CommentPublic
from src.tasks.schemas import TaskPublic


class CommentWithTask(CommentPublic):
    task: Optional[TaskPublic] = None
