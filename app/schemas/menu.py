from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# =====================================================================
# SCHEMAS CHO MÓN ĂN (MenuItems - TSK-27 / PBI-16)
# =====================================================================

class MenuItemBase(BaseModel):
    """Schema cơ sở cho Món ăn"""
    name: str = Field(..., min_length=1, max_length=150, description="Tên món ăn")
    description: Optional[str] = Field(None, description="Mô tả nguyên liệu, hương vị món ăn")
    price: float = Field(..., ge=0, description="Đơn vị giá món ăn (VND, không được âm)")
    image_url: Optional[str] = Field(None, max_length=500, description="Đường dẫn ảnh món ăn")
    is_available: bool = Field(True, description="Trạng thái phục vụ: True = Còn món, False = Hết món")

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Tên món ăn không được để trống.")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Giá tiền món ăn không được âm.")
        return v


class MenuItemCreate(MenuItemBase):
    """Schema yêu cầu tạo món ăn mới"""
    pass


class MenuItemUpdate(BaseModel):
    """Schema yêu cầu cập nhật thông tin món ăn"""
    name: Optional[str] = Field(None, min_length=1, max_length=150, description="Tên món ăn")
    description: Optional[str] = Field(None, description="Mô tả món ăn")
    price: Optional[float] = Field(None, ge=0, description="Đơn giá mới (VND)")
    image_url: Optional[str] = Field(None, max_length=500, description="Đường dẫn ảnh món ăn")
    is_available: Optional[bool] = Field(None, description="Trạng thái còn món hay hết món")

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Tên món ăn không được để trống.")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Giá tiền món ăn không được âm.")
        return v


class MenuItemAvailabilityUpdate(BaseModel):
    """Schema cập nhật nhanh trạng thái còn món (Patch Availability)"""
    is_available: bool = Field(..., description="True = Còn món, False = Tạm hết")


class MenuItemResponse(MenuItemBase):
    """Schema phản hồi thông tin món ăn từ CSDL"""
    id: int
    menu_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================================
# SCHEMAS CHO NHÓM THỰC ĐƠN (RestaurantMenus - TSK-27 / PBI-16)
# =====================================================================

class RestaurantMenuBase(BaseModel):
    """Schema cơ sở cho Nhóm thực đơn"""
    name: str = Field(..., min_length=1, max_length=100, description="Tên nhóm thực đơn (VD: Món Khai Vị, Đồ Uống)")
    description: Optional[str] = Field(None, max_length=255, description="Mô tả nhóm thực đơn")
    display_order: int = Field(0, description="Thứ tự hiển thị (tăng dần)")

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Tên nhóm thực đơn không được để trống.")
        return v


class RestaurantMenuCreate(RestaurantMenuBase):
    """Schema yêu cầu tạo nhóm thực đơn mới cho nhà hàng"""
    pass


class RestaurantMenuUpdate(BaseModel):
    """Schema yêu cầu cập nhật nhóm thực đơn"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Tên nhóm thực đơn")
    description: Optional[str] = Field(None, max_length=255, description="Mô tả nhóm thực đơn")
    display_order: Optional[int] = Field(None, description="Thứ tự hiển thị")

    @field_validator("name")
    def validate_name(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Tên nhóm thực đơn không được để trống.")
        return v


class RestaurantMenuResponse(RestaurantMenuBase):
    """Schema phản hồi thông tin nhóm thực đơn"""
    id: int
    restaurant_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RestaurantMenuWithItemsResponse(RestaurantMenuResponse):
    """Schema phản hồi nhóm thực đơn kèm đầy đủ danh sách món ăn con"""
    items: List[MenuItemResponse] = Field(default_factory=list, description="Danh sách món ăn thuộc nhóm này")

    class Config:
        from_attributes = True
