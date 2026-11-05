"""User profile management API module.

Provides RESTful endpoints for retrieving and updating user profile metadata
and default geolocation settings used by the recommendation engine.
"""

from datetime import date
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="FoodAI Service - User Profile API",
    description="RESTful API quản lý hồ sơ người dùng và cấu hình tọa độ mặc định.",
    version="1.0.0",
)

# Cho phép CORS toàn cục trên môi trường local/staging để Frontend tách rời gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfileUpdateSchema(BaseModel):
    """Payload validation schema cho request cập nhật hồ sơ (PUT)."""

    full_name: str = Field(..., min_length=2, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field("Nam", max_length=20)
    date_of_birth: Optional[date] = Field(None)
    default_address: Optional[str] = Field(None, max_length=255)
    # Giới hạn dải tọa độ chuẩn WGS84 (SRID 4326) để tránh lỗi khi truy vấn Spatial Index
    default_lat: Optional[float] = Field(None, ge=-90.0, le=90.0)
    default_lng: Optional[float] = Field(None, ge=-180.0, le=180.0)


class UserProfileResponseSchema(UserProfileUpdateSchema):
    """Schema trả về kết hợp dữ liệu từ bảng Users và UserProfiles (1-1)."""

    profile_id: int
    user_id: int
    email: str
    phone: str
    status: str


# In-memory store giả lập bản ghi từ bảng Users JOIN UserProfiles
# Sẽ được thay thế bằng Dependency Injection (SQLAlchemy Session) khi kết nối MySQL
MOCK_USER_PROFILE = {
    "profile_id": 2,
    "user_id": 2,
    "email": "user.demo@foodai.vn",
    "phone": "0901234568",
    "status": "active",
    "full_name": "Nguyễn Văn An",
    "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=240&q=80",
    "gender": "Nam",
    "date_of_birth": "2000-01-15",
    "default_address": "11 Nguyễn Đình Chiểu, Phường Đa Kao, Quận 1, TP. Hồ Chí Minh",
    "default_lat": 10.7860000,
    "default_lng": 106.7003000,
}


@app.get("/api/users/profile", response_model=UserProfileResponseSchema, tags=["User Profile"])
async def get_user_profile(user_id: int = 2):
    """Truy xuất hồ sơ cá nhân theo user_id (mặc định lấy từ context xác thực)."""
    if user_id != MOCK_USER_PROFILE["user_id"]:
        raise HTTPException(status_code=404, detail="User profile not found.")
    return MOCK_USER_PROFILE


@app.put("/api/users/profile", response_model=UserProfileResponseSchema, tags=["User Profile"])
async def update_user_profile(payload: UserProfileUpdateSchema, user_id: int = 2):
    """Cập nhật thông tin cá nhân và vị trí mặc định phục vụ tính khoảng cách gợi ý."""
    if user_id != MOCK_USER_PROFILE["user_id"]:
        raise HTTPException(status_code=404, detail="User profile not found.")

    MOCK_USER_PROFILE.update({
        "full_name": payload.full_name,
        "avatar_url": payload.avatar_url,
        "gender": payload.gender,
        "date_of_birth": str(payload.date_of_birth) if payload.date_of_birth else None,
        "default_address": payload.default_address,
        "default_lat": payload.default_lat,
        "default_lng": payload.default_lng,
    })
    return MOCK_USER_PROFILE