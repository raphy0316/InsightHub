from fastapi import FastAPI
from app.routers.health import router as health_router

app = FastAPI(title="InsightHub API (minimal)", version="0.1")
app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "ok"}



