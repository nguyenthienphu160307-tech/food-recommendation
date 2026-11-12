from .auth import router as auth_router
from .restaurant import router as restaurant_router
from .profile_api import router as profile_router
from .geo import router as geo_router
from .ai_search import router as ai_search_router
from .users import router as users_router

__all__ = ["auth_router", "profile_router", "geo_router", "ai_search_router"]