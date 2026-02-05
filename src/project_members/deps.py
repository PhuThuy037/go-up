from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel

from src.auth.deps import CurrentUser
from src.project_members.project_role import ProjectRole


@dataclass(frozen=True)
class MemberCtx:
    project_id: int
    user_id: int
    current_user_id: int

class AddMemberBody(SQLModel):
    user_id: int
    role: ProjectRole | None = None

def get_member_ctx(project_id: int, user_id: int, current_user: CurrentUser) -> MemberCtx:
    return MemberCtx(project_id=project_id, user_id=user_id, current_user_id=current_user.id)

MemberCtxDeps = Annotated[MemberCtx, Depends(get_member_ctx)]