from sqlmodel import create_engine, Session
from typing import Generator

from config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
