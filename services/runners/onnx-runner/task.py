from worker import app
import logging
import os

logger = logging.getLogger(__name__)

@app.task(name="onnx.test_ping")
def test_ping(payload: dict = None) -> dict:
    logger.info("ONNX Test Ping")
    return {
        "status": "ok",
        "worker": "onnx-runner",
        "dry_run": os.getenv("DRY_RUN", "0"),
        "payload": payload
    }