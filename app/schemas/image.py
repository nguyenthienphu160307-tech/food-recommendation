from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# =====================================================================
# SCHEMAS CHO HÌNH ẢNH NHÀ HÀNG (RestaurantImages - TSK-28 / PBI-16)
# =====================================================================

class RestaurantImageBase(BaseModel):
    """Schema cơ sở cho hình ảnh nhà hàng"""
    image_url: str = Field(..., min_length=1, max_length=500, description="Đường dẫn ảnh (URL hoặc đường dẫn tĩnh)")
    caption: Optional[str] = Field(None, max_length=255, description="Chú thích ảnh (VD: 'Không gian ngoài trời', 'Mặt tiền quán')")
    is_cover: bool = Field(False, description="Cờ đánh dấu ảnh đại diện / ảnh bìa chính")
    display_order: int = Field(0, ge=0, description="Thứ tự hiển thị (số nguyên tăng dần)")

    @field_validator("image_url")
    def validate_url(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Đường dẫn hình ảnh không được để trống.")
        return v


class RestaurantImageCreate(RestaurantImageBase):
    """Schema yêu cầu thêm 1 ảnh mới bằng URL"""
    pass


class RestaurantImageBatchCreate(BaseModel):
    """Schema yêu cầu thêm nhiều ảnh cùng lúc bằng danh sách URL"""
    images: List[RestaurantImageCreate] = Field(..., min_length=1, description="Danh sách các ảnh cần thêm")


class RestaurantImageUpdate(BaseModel):
    """Schema yêu cầu cập nhật thông tin ảnh (chú thích, thứ tự hiển thị)"""
    caption: Optional[str] = Field(None, max_length=255, description="Chú thích ảnh mới")
    display_order: Optional[int] = Field(None, ge=0, description="Thứ tự hiển thị mới")


class SetCoverResponse(BaseModel):
    """Phản hồi sau khi cập nhật ảnh bìa chính"""
    image_id: int
    restaurant_id: int
    is_cover: bool
    message: str


class RestaurantImageResponse(RestaurantImageBase):
    """Schema phản hồi thông tin chi tiết một bức ảnh"""
    id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        from_attributes = True
