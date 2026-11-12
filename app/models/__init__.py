# filepath: app/models/__init__.py
from .user import User, UserProfile, Role, UserRole, OTPStorage, RevokedToken
from .interaction import Restaurant

__all__ = [
    "User",
    "UserProfile",
    "Role",
    "UserRole",
    "OTPStorage",
    "RevokedToken",
    "Restaurant",
]