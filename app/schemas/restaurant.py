from typing import Optional, List
from pydantic import BaseModel, Field


class AmenityResponse(BaseModel):
    """Schema 5 tiện ích chính của nhà hàng"""
    has_parking: bool = Field(False, description="Có chỗ đậu ô tô")
    has_private_room: bool = Field(False, description="Có phòng riêng")
    has_outdoor: bool = Field(False, description="Có không gian ngoài trời")
    pet_friendly: bool = Field(False, description="Thân thiện với thú cưng")
    vegetarian_support: bool = Field(False, description="Có hỗ trợ món chay")

    class Config:
        from_attributes = True


class RestaurantListItemResponse(BaseModel):
    """Schema thông tin tóm tắt nhà hàng trả về trong danh sách"""
    id: int
    name: str
    description: Optional[str] = None
    address: str
    phone_number: Optional[str] = None
    cuisine_type: Optional[str] = None
    latitude: float
    longitude: float
    min_price: float
    max_price: float
    open_hours: Optional[str] = None
    avg_rating: float
    total_reviews: int
    status: str
    cover_image_url: Optional[str] = Field(None, description="Đường dẫn ảnh bìa (is_cover=True)")
    amenities: Optional[AmenityResponse] = Field(None, description="Các cờ tiện ích chính")
    
    # BR-03: Trạng thái mở cửa hoạt động thực tế & điểm thưởng xếp hạng
    is_open: bool = Field(default=False, description="Nhà hàng có đang mở cửa tại thời điểm hiện tại không (BR-03)")
    open_status_label: Optional[str] = Field(default=None, description="Nhãn hiển thị trạng thái: 'Đang mở cửa' hoặc 'Đã đóng cửa'")
    open_status_detail: Optional[str] = Field(default=None, description="Chi tiết thời gian: 'Mở cửa đến 22:00', 'Mở lại lúc 17:00'...")
    ranking_bonus: float = Field(default=0.0, description="Điểm thưởng cộng vào xếp hạng Weighted Score (BR-03)")

    class Config:
        from_attributes = True


class RestaurantOpenStatusResponse(BaseModel):
    """Schema chi tiết trạng thái giờ mở cửa phục vụ kiểm tra thời gian thực (BR-03)"""
    restaurant_id: int
    restaurant_name: str
    open_hours_raw: Optional[str] = None
    is_open: bool
    status_code: str
    status_label: str
    detail_text: str
    badge_color: str
    bonus_score: float
    checked_at: str


class PaginationMetadata(BaseModel):
    """Metadata thông tin phân trang"""
    page: int = Field(..., description="Trang hiện tại (1-based)")
    limit: int = Field(..., description="Số lượng mục trên mỗi trang")
    total_items: int = Field(..., description="Tổng số nhà hàng")
    total_pages: int = Field(..., description="Tổng số trang")


class RestaurantListResponse(BaseModel):
    """Phản hồi danh sách nhà hàng kèm phân trang chuẩn RESTful"""
    data: List[RestaurantListItemResponse]
    pagination: PaginationMetadata
