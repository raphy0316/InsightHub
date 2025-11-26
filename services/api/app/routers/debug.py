from fastapi import APIRouter
from celery import Celery
import os

router = APIRouter(prefix="/debug", tags=["debug"])

celery_app = Celery(
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_BACKEND_URL"]
)

@router.get("/onnx-ping")
def onnx_ping():
    result = celery_app.send_task(
        "onnx.test_ping",
        kwargs={"payload": {"message": "Hello, ONNX!"}},
        queue=os.getenv("QUEUE_ONNX", "onnx")
    )

    return {
        "task_id": result.id,
        "status": "sent",
        "message": "ONNX Test Ping sent"
    }

@router.get("/onnx-ping/{task_id}")
def onnx_ping_result(task_id: str):
    result = celery_app.AsyncResult(task_id)

    return {
        "task_id": result.id,
        "status": result.status,
        "result": result.result if result.ready() else "not ready"
    }