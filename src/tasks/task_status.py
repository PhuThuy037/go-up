from enum import Enum

class TaskStatus(str, Enum):
    DOING = "doing"
    COMPLETED = "completed"
    TODO= "todo"