from .health import router as health_router
from .auth import router as auth_router
from .project import router as project_router

__all__ = ["health_router", "auth_router", "project_router"]
