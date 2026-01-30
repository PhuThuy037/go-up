from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.auth.router import router as user_router
import src.all_models
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 App starting...")
    yield
    # Shutdown
    print("🛑 App shutting down...")

app = FastAPI()

# Router
app.include_router(user_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
