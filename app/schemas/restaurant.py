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

    class Config:
        from_attributes = True


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


class RestaurantFilterItemResponse(RestaurantListItemResponse):
    """Schema thông tin nhà hàng trả về khi lọc đa điều kiện kèm khoảng cách GPS"""
    distance_km: Optional[float] = Field(None, description="Khoảng cách từ vị trí người dùng đến nhà hàng (km)")


class AppliedFilterCriteria(BaseModel):
    """Tóm tắt các điều kiện lọc đã áp dụng (FR-07 / UC-04)"""
    keyword: Optional[str] = None
    cuisine_type: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    radius_km: Optional[float] = None
    min_rating: Optional[float] = None
    has_parking: Optional[bool] = None
    has_private_room: Optional[bool] = None
    has_outdoor: Optional[bool] = None
    pet_friendly: Optional[bool] = None
    vegetarian_support: Optional[bool] = None
    sort_by: str = "default"
    status_filter: str = "active"


class RestaurantFilterResponse(BaseModel):
    """Phản hồi API lọc nhà hàng đa điều kiện kết hợp (TE9C660)"""
    status: str = "success"
    data: List[RestaurantFilterItemResponse]
    applied_filters: AppliedFilterCriteria
    pagination: PaginationMetadata


class RestaurantImageResponse(BaseModel):
    """Schema hình ảnh trong bộ sưu tập slide của nhà hàng (RestaurantImages - FR-09)"""
    id: int
    image_url: str
    caption: Optional[str] = None
    is_cover: bool = False
    display_order: int = 0

    class Config:
        from_attributes = True


class MenuItemResponse(BaseModel):
    """Schema món ăn chi tiết trong thực đơn (MenuItems - FR-09)"""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True

    class Config:
        from_attributes = True


class RestaurantMenuResponse(BaseModel):
    """Schema nhóm danh mục thực đơn (RestaurantMenus - FR-09)"""
    id: int
    name: str
    description: Optional[str] = None
    display_order: int = 0
    items: List[MenuItemResponse] = Field(default_factory=list, description="Danh sách món ăn thuộc nhóm")

    class Config:
        from_attributes = True


class RestaurantDetailResponse(BaseModel):
    """Schema phản hồi chi tiết toàn diện của Nhà hàng (FR-09 / TE9C662)"""
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
    cover_image_url: Optional[str] = Field(None, description="Ảnh bìa chính đại diện")
    distance_km: Optional[float] = Field(None, description="Khoảng cách GPS tính từ vị trí người dùng (km)")
    amenities: Optional[AmenityResponse] = Field(None, description="5 tiện ích của nhà hàng")
    images: List[RestaurantImageResponse] = Field(default_factory=list, description="Bộ ảnh slide của nhà hàng")
    menus: List[RestaurantMenuResponse] = Field(default_factory=list, description="Thực đơn phân theo nhóm danh mục")

    class Config:
        from_attributes = True

