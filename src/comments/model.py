from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from src.util.util import utc_now

if TYPE_CHECKING:
    from src.auth.model import User
    from src.tasks.model import Task


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(..., description="Nội dung bình luận")
    created_at: datetime = Field(default_factory=utc_now)

    # 3. Khóa ngoại (Liên kết tới ai? Task nào?)
    user_id: int = Field(foreign_key="users.id")
    task_id: int = Field(foreign_key="tasks.id")

    # 4. Relationships (Để truy vấn ngược xuôi)
    # Lấy thông tin người chat (Avatar, Tên) từ comment này
    user: "User" = Relationship(back_populates="comments")

    # Lấy thông tin task từ comment này (ít dùng hơn, nhưng cứ khai báo cho đủ bộ)
    task: "Task" = Relationship(back_populates="comments")