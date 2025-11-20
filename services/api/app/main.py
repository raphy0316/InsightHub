# app/main.py
from fastapi import FastAPI, Response as FastAPIResponse, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from .routers.health import router as health_router
from .routers.auth import router as auth_router

from .schemas.common import Response as APIResponse

import time

app = FastAPI(title="InsightHub API", version="0.1")

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Middleware to track request metrics"""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    # Track metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()

    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    return response


@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return FastAPIResponse(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """
    모든 HTTPException을 통일된 Response 형태로 래핑
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            message=str(exc.detail),
            data=None,
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):

    return JSONResponse(
        status_code=422,
        content=APIResponse(
            success=False,
            message="Validation error",
            data=exc.errors(), # front can use this to show validation issues
        ).model_dump(),
    )


app.include_router(health_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "ok"}
