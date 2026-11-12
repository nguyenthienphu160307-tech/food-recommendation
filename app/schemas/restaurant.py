from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


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

    model_config = ConfigDict(from_attributes=True)


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
    menus: List[MenuCategoryResponse] = []
    images: List[RestaurantImageResponse] = []