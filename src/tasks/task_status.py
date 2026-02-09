from enum import Enum


class TaskStatus(str, Enum):
    doing = "doing"
    completed = "completed"
    todo = "todo"
