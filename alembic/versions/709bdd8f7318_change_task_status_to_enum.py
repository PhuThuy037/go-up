from alembic import op
from sqlalchemy.dialects import postgresql

revision = "709bdd8f7318"
down_revision = "869cb756732d"

ENUM_NAME = "task_status"

def upgrade() -> None:
    # 1) Tạo ENUM type với các VALUES đúng theo TaskStatus.value
    task_status = postgresql.ENUM(
        "todo", "doing", "completed",
        name=ENUM_NAME
    )
    task_status.create(op.get_bind(), checkfirst=True)

    # 2) (Quan trọng) Normalize data cũ nếu DB đang có "Todo"/"Done" kiểu khác
    # Nếu bạn chắc DB chỉ có todo/doing/completed thì bỏ step này.
    op.execute("""
        UPDATE tasks
        SET status = lower(status)
        WHERE status IS NOT NULL
    """)

    # 3) Alter column sang ENUM + cast
    op.execute(f"""
        ALTER TABLE tasks
        ALTER COLUMN status TYPE {ENUM_NAME}
        USING status::{ENUM_NAME}
    """)

    # 4) Default (optional)
    op.execute("ALTER TABLE tasks ALTER COLUMN status SET DEFAULT 'todo'")


def downgrade() -> None:
    op.execute("ALTER TABLE tasks ALTER COLUMN status DROP DEFAULT")

    # enum -> text
    op.execute("""
        ALTER TABLE tasks
        ALTER COLUMN status TYPE TEXT
        USING status::text
    """)

    task_status = postgresql.ENUM(
        "todo", "doing", "completed",
        name=ENUM_NAME
    )
    task_status.drop(op.get_bind(), checkfirst=True)
