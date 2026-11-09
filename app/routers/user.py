from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.user import User, UserProfile
from app.schemas.user import UserProfileUpdateSchema, UserProfileResponseSchema

router = APIRouter(prefix="/api/users", tags=["Hồ sơ người dùng (UserProfiles)"])


@router.get(
    "/profile",
    response_model=UserProfileResponseSchema,
    summary="Lấy thông tin hồ sơ cá nhân (PBI-03 / TSK-04)"
)
def get_user_profile(
    email: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin hồ sơ người dùng từ bảng Users và UserProfiles:
    - Nếu truyền email hoặc user_id -> Lấy đúng hồ sơ tài khoản đó.
    - Nếu không truyền -> Lấy tài khoản người dùng hoạt động gần nhất.
    """
    query = db.query(User)
    if user_id:
        user = query.filter(User.id == user_id).first()
    elif email:
        user = query.filter(User.email == email.strip().lower()).first()
    else:
        user = query.order_by(User.id.desc()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy tài khoản người dùng tương ứng."
        )

    profile = user.profile
    if not profile:
        profile = UserProfile(
            user_id=user.id,
            full_name=user.email.split("@")[0] if user.email else "Người dùng"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return UserProfileResponseSchema(
        profile_id=profile.id,
        user_id=user.id,
        email=user.email,
        phone=user.phone_number,
        status=user.status,
        full_name=profile.full_name,
        avatar_url=profile.avatar_url or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
        default_address=profile.default_address or "11 Nguyễn Đình Chiểu, Phường Đa Kao, Quận 1, TP.HCM",
        default_lat=profile.default_lat or 10.7860000,
        default_lng=profile.default_lng or 106.7003000
    )


@router.put(
    "/profile",
    response_model=UserProfileResponseSchema,
    summary="Cập nhật thông tin hồ sơ & Tọa độ mặc định (PBI-03 / TSK-04)"
)
def update_user_profile(
    payload: UserProfileUpdateSchema,
    db: Session = Depends(get_db)
):
    """
    Cập nhật Họ tên, ảnh đại diện, địa chỉ & tọa độ GPS mặc định vào bảng UserProfiles:
    - Tìm tài khoản theo email hoặc user_id hoặc tài khoản gần nhất.
    - Lưu lại vào CSDL MySQL.
    """
    query = db.query(User)
    if payload.user_id:
        user = query.filter(User.id == payload.user_id).first()
    elif payload.email:
        user = query.filter(User.email == payload.email.strip().lower()).first()
    else:
        user = query.order_by(User.id.desc()).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy tài khoản người dùng để cập nhật."
        )

    profile = user.profile
    if not profile:
        profile = UserProfile(user_id=user.id, full_name=payload.full_name)
        db.add(profile)
        db.flush()

    # Cập nhật các trường thông tin
    profile.full_name = payload.full_name
    if payload.avatar_url:
        profile.avatar_url = payload.avatar_url
    if payload.default_address is not None:
        profile.default_address = payload.default_address
    if payload.default_lat is not None:
        profile.default_lat = payload.default_lat
    if payload.default_lng is not None:
        profile.default_lng = payload.default_lng

    db.commit()
    db.refresh(profile)

    return UserProfileResponseSchema(
        profile_id=profile.id,
        user_id=user.id,
        email=user.email,
        phone=user.phone_number,
        status=user.status,
        full_name=profile.full_name,
        avatar_url=profile.avatar_url,
        gender=payload.gender or "Nam",
        date_of_birth=payload.date_of_birth,
        default_address=profile.default_address,
        default_lat=profile.default_lat,
        default_lng=profile.default_lng
    )
