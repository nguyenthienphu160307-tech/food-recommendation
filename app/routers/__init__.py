from .auth import router as auth_router
from .restaurant import router as restaurant_router
from .profile_api import router as profile_router
from .geo import router as geo_router
from .ai_search import router as ai_search_router
from .users import router as users_router
from .search import router as search_router, search_history_router
from .admin import admin_router
from .preferences import router as preferences_router
from .notification import router as notification_router
from .review import router as review_router
from .image import router as image_router
from .menu import router as menu_router
from .favorite import router as favorite_router

__all__ = [
    "auth_router",
    "restaurant_router",
    "profile_router",
    "geo_router",
    "ai_search_router",
    "users_router",
    "search_router",
    "search_history_router",
    "admin_router",
    "preferences_router",
    "notification_router",
    "review_router",
    "image_router",
    "menu_router",
    "favorite_router",
]
