from typing import Optional
from pydantic import BaseModel, Field

class UserProfileUpdateSchema(BaseModel):
    """Schema cập nhật hồ sơ cá nhân và tọa độ mặc định (PBI-03 / TSK-04)"""
    email: Optional[str] = Field(None, description="Email người dùng để định danh tài khoản")
    user_id: Optional[int] = Field(None, description="ID người dùng")
    full_name: str = Field(..., min_length=2, max_length=100, description="Họ và tên hiển thị")
    avatar_url: Optional[str] = Field(None, max_length=500, description="Đường dẫn ảnh đại diện")
    gender: Optional[str] = Field("Nam", max_length=20, description="Giới tính")
    date_of_birth: Optional[str] = Field(None, description="Ngày sinh")
    default_address: Optional[str] = Field(None, max_length=255, description="Địa chỉ mặc định")
    default_lat: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Vĩ độ mặc định (Latitude)")
    default_lng: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Kinh độ mặc định (Longitude)")


class UserProfileResponseSchema(BaseModel):
    """Schema phản hồi thông tin hồ sơ cá nhân hoàn chỉnh"""
    profile_id: int
    user_id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    status: str
    full_name: str
    avatar_url: Optional[str] = None
    gender: Optional[str] = "Nam"
    date_of_birth: Optional[str] = None
    default_address: Optional[str] = None
    default_lat: Optional[float] = None
    default_lng: Optional[float] = None

    class Config:
        from_attributes = True
