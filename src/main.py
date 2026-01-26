from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 App starting...")
    yield
    # Shutdown
    print("🛑 App shutting down...")

app = FastAPI()

# Router
# app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
