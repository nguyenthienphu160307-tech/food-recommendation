from .auth import router as auth_router
from .restaurant import router as restaurant_router
from .user import router as user_router
from .search import router as search_router, search_history_router
from .menu import router as menu_router
from .image import router as image_router
from .notification import router as notification_router

__all__ = [
    "auth_router",
    "restaurant_router",
    "user_router",
    "search_router",
    "search_history_router",
    "menu_router",
    "image_router",
    "notification_router",
]
