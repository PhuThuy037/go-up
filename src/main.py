from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.auth.router import router as user_router
from src.comments.router import router as comment_router
from src.common.errors import AppError
from src.common.handlers import (
    app_error_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_error_handler,
)
from src.project_members.router import router as project_member_router
from src.projects.router import router as project_router
from src.tasks.router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 App starting...")
    yield
    # Shutdown
    print("🛑 App shutting down...")


app = FastAPI()

# Handle error
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# Router
app.include_router(user_router)
app.include_router(task_router)
app.include_router(project_router)
app.include_router(project_member_router)
app.include_router(comment_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
