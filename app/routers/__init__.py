from .auth import router as auth_router
from .admin import admin_router

__all__ = ["auth_router", "admin_router"]
