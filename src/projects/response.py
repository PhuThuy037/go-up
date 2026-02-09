from typing import List, Optional

from src.auth.schemas import UserPublic
from src.projects.schemas import ProjectPublic
from src.tasks.schemas import TaskPublic


class ProjectWithTasks(ProjectPublic):
    tasks: Optional[List[TaskPublic]] = []


class ProjectWithUsers(ProjectPublic):
    members: Optional[List[UserPublic]] = []
