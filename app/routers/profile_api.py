"""User profile management API module.

Provides RESTful endpoints for retrieving and updating user profile metadata
and default geolocation settings used by the recommendation engine.
"""

# filepath: app/routers/profile_api.py
from datetime import date
from typing import Optional
from urllib.parse import quote_plus
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rbac import get_current_guest_or_user
from app.models.user import User, UserProfile

router = APIRouter(prefix="/api/users", tags=["User Profile"])


class UserProfileUpdateSchema(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    gender: Optional[str] = Field("Nam", max_length=20)
    date_of_birth: Optional[date] = Field(None)
    default_address: Optional[str] = Field(None, max_length=255)
    default_lat: Optional[float] = Field(None, ge=-90.0, le=90.0)
    default_lng: Optional[float] = Field(None, ge=-180.0, le=180.0)
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserProfileResponseSchema(UserProfileUpdateSchema):
    profile_id: int
    user_id: int
    email: str
    phone: str
    status: str


@router.get("/profile", response_model=UserProfileResponseSchema)
def get_user_profile(
    user_id: Optional[int] = None,
    email: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_guest_or_user),
    db: Session = Depends(get_db)
):
    target_user: Optional[User] = None
    if isinstance(current_user, User):
        target_user = current_user
    elif email:
        target_user = db.query(User).filter(User.email == email).first()
    elif user_id:
        target_user = db.query(User).filter(User.id == user_id).first()

    if not target_user:
        target_user = db.query(User).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found."
            )

    profile = target_user.profile
    if not profile:
        profile = UserProfile(
            user_id=target_user.id,
            full_name=target_user.email.split("@")[0] if target_user.email else "Người dùng"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    avatar = profile.avatar_url
    if not avatar:
        avatar = f"https://ui-avatars.com/api/?name={quote_plus(profile.full_name or target_user.email or 'User')}&background=E11D48&color=fff&bold=true"

    return UserProfileResponseSchema(
        profile_id=profile.id,
        user_id=target_user.id,
        email=target_user.email or "",
        phone=target_user.phone_number or "",
        status=target_user.status or "active",
        full_name=profile.full_name,
        avatar_url=avatar,
        gender="Nam",
        date_of_birth=None,
        default_address=profile.default_address or "",
        default_lat=profile.default_lat or 10.776889,
        default_lng=profile.default_lng or 106.700806,
    )


@router.put("/profile", response_model=UserProfileResponseSchema)
def update_user_profile(
    payload: UserProfileUpdateSchema,
    user_id: Optional[int] = None,
    email: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_guest_or_user),
    db: Session = Depends(get_db)
):
    target_user: Optional[User] = None
    if isinstance(current_user, User):
        target_user = current_user
    elif payload.user_id or user_id:
        uid = payload.user_id or user_id
        target_user = db.query(User).filter(User.id == uid).first()
    elif payload.email or email:
        em = payload.email or email
        target_user = db.query(User).filter(User.email == em).first()

    if not target_user:
        target_user = db.query(User).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found."
            )

    profile = target_user.profile
    if not profile:
        profile = UserProfile(
            user_id=target_user.id,
            full_name=payload.full_name
        )
        db.add(profile)
    else:
        profile.full_name = payload.full_name

    if payload.avatar_url is not None:
        profile.avatar_url = payload.avatar_url
    if payload.default_address is not None:
        profile.default_address = payload.default_address
    if payload.default_lat is not None:
        profile.default_lat = payload.default_lat
    if payload.default_lng is not None:
        profile.default_lng = payload.default_lng

    db.commit()
    db.refresh(profile)

    avatar = profile.avatar_url
    if not avatar:
        avatar = f"https://ui-avatars.com/api/?name={quote_plus(profile.full_name or 'User')}&background=E11D48&color=fff&bold=true"

    return UserProfileResponseSchema(
        profile_id=profile.id,
        user_id=target_user.id,
        email=target_user.email or "",
        phone=target_user.phone_number or "",
        status=target_user.status or "active",
        full_name=profile.full_name,
        avatar_url=avatar,
        gender=payload.gender or "Nam",
        date_of_birth=payload.date_of_birth,
        default_address=profile.default_address or "",
        default_lat=profile.default_lat or 10.776889,
        default_lng=profile.default_lng or 106.700806,
    )
