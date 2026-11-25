from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.menu import RestaurantMenuResponse


class AmenityResponse(BaseModel):
    """Schema 5 tiện ích chính của nhà hàng"""
    has_parking: bool = Field(False, description="Có chỗ đậu ô tô")
    has_private_room: bool = Field(False, description="Có phòng riêng")
    has_outdoor: bool = Field(False, description="Có không gian ngoài trời")
    pet_friendly: bool = Field(False, description="Thân thiện với thú cưng")
    vegetarian_support: bool = Field(False, description="Có hỗ trợ món chay")

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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


class MenuItemResponse(BaseModel):
    """Một món ăn trong thực đơn"""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True

    model_config = ConfigDict(from_attributes=True)


class MenuCategoryResponse(BaseModel):
    """Nhóm món (Khai vị, Món chính, Đồ uống...) kèm danh sách món"""
    id: int
    name: str
    description: Optional[str] = None
    display_order: int = 0
    items: List[MenuItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class RestaurantImageResponse(BaseModel):
    """Một ảnh trong thư viện ảnh của nhà hàng"""
    id: int
    image_url: str
    caption: Optional[str] = None
    is_cover: bool = False
    display_order: int = 0

    model_config = ConfigDict(from_attributes=True)


class RestaurantDetailResponse(RestaurantListItemResponse):
    """Chi tiết một nhà hàng: thông tin cơ bản + thực đơn + thư viện ảnh"""
    distance_km: Optional[float] = Field(None, description="Khoảng cách từ vị trí người dùng đến nhà hàng (km)")
    menus: List[MenuCategoryResponse] = []
    images: List[RestaurantImageResponse] = []


class AmenityUpdateRequest(BaseModel):
    """Schema dữ liệu gửi lên khi Admin cập nhật tiện ích nhà hàng."""
    has_parking: Optional[bool] = Field(None, description="Có chỗ đậu ô tô")
    has_private_room: Optional[bool] = Field(None, description="Có phòng riêng")
    has_outdoor: Optional[bool] = Field(None, description="Có không gian ngoài trời")
    pet_friendly: Optional[bool] = Field(None, description="Thân thiện với thú cưng")
    vegetarian_support: Optional[bool] = Field(None, description="Có hỗ trợ món chay")


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
    """Phản hồi API lọc nhà hàng đa điều kiện kết hợp (TE9C660, TE9C66F)"""
    status: str = "success"
    total: Optional[int] = Field(None, description="Tổng số nhà hàng khớp điều kiện (alias của pagination.total_items)")
    data: List[RestaurantFilterItemResponse]
    applied_filters: AppliedFilterCriteria
    pagination: PaginationMetadata