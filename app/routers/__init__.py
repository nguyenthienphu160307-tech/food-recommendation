from .auth import router as auth_router
from .admin import admin_router
from .preferences import router as preferences_router

__all__ = ["auth_router", "admin_router", "preferences_router"]
