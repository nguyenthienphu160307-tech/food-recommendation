from .auth import router as auth_router
from .profile_api import router as profile_router
from .geo import router as geo_router
from .ai_search import router as ai_search_router
from .restaurant import router as restaurant_router
from .user import router as user_router
from .search import router as search_router

__all__ = [
    "auth_router",
    "profile_router",
    "geo_router",
    "ai_search_router",
    "restaurant_router",
    "user_router",
    "search_router",
]