from .auth import router as auth_router
from .restaurant import router as restaurant_router
from .user import router as user_router
from .search import router as search_router
from .menu import router as menu_router
from .image import router as image_router

__all__ = ["auth_router", "restaurant_router", "user_router", "search_router", "menu_router", "image_router"]
