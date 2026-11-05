from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

app = FastAPI(
    title="FoodAI - Module 1: UserProfiles API",
    description="API Quản lý Hồ sơ cá nhân (Task TE9C64D - PBI-03)",
    version="1.0.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema Pydantic chuẩn theo bảng UserProfiles trong CSDL
class UserProfileUpdateSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="Họ và tên hiển thị")
    avatar_url: Optional[str] = Field(None, max_length=255, description="Đường dẫn ảnh đại diện")
    gender: Optional[str] = Field("Nam", max_length=20, description="Giới tính: Nam / Nữ / Khác")
    date_of_birth: Optional[date] = Field(None, description="Ngày sinh (YYYY-MM-DD)")
    default_address: Optional[str] = Field(None, max_length=255, description="Địa chỉ mặc định")
    default_lat: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Vĩ độ mặc định (Latitude)")
    default_lng: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Kinh độ mặc định (Longitude)")

class UserProfileResponseSchema(UserProfileUpdateSchema):
    profile_id: int
    user_id: int
    email: str
    phone: str
    status: str

# Dữ liệu mẫu đồng bộ với bảng Users & UserProfiles trong seed_data.sql
MOCK_USER_PROFILE = {
    "profile_id": 2,
    "user_id": 2,
    "email": "admin@foodai.vn",
    "phone": "0912345678",
    "status": "active",
    "full_name": "Nguyễn Văn A",
    "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=ThienPhu",
    "gender": "Nam",
    "date_of_birth": "2007-03-30",
    "default_address": "Số 11 Nguyễn Đình Chiểu, Đa Kao, Thành phố Hồ Chí Mình",
    "default_lat": 10.8386000,
    "default_lng": 106.6652000
}

@app.get("/api/users/profile", response_model=UserProfileResponseSchema, tags=["UserProfiles"])
async def get_user_profile(user_id: int = 2):
    """
    Lấy thông tin hồ sơ cá nhân của người dùng hiện tại từ bảng UserProfiles.
    """
    if user_id != MOCK_USER_PROFILE["user_id"]:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ người dùng (UserProfiles)")
    return MOCK_USER_PROFILE

@app.put("/api/users/profile", response_model=UserProfileResponseSchema, tags=["UserProfiles"])
async def update_user_profile(payload: UserProfileUpdateSchema, user_id: int = 2):
    if user_id != MOCK_USER_PROFILE["user_id"]:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ người dùng")

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