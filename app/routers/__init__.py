from .auth import router as auth_router
from .restaurant import router as restaurant_router
from .user import router as user_router
from .search import router as search_router

__all__ = ["auth_router", "restaurant_router", "user_router", "search_router"]
