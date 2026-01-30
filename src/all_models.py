# src/all_models.py

# Thứ tự import ở đây vẫn cần chuẩn (Lá trước, Gốc sau) để tránh lỗi vòng lặp
from src.project_members.model import ProjectMember
from src.projects.model import Project
from src.tasks.model import Task
from src.comments.model import Comment
from src.auth.model import User

# File này không cần làm gì cả, chỉ cần import để các class được đăng ký vào SQLModel