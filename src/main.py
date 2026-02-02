from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from src.auth.router import router as user_router
from src.projects.router import router as project_router
from fastapi.exceptions import RequestValidationError
from src.common.errors import AppError
import src.all_models
from src.common.handlers import (
    app_error_handler,
    validation_error_handler,
    http_exception_handler,
    unhandled_exception_handler,
)

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
app.include_router(project_router)



@app.get("/health")
def health_check():
    return {"status": "ok"}
