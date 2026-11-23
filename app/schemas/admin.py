"""
Schema cho Quản trị viên & Báo cáo Thống kê Dashboard (Task TE9C67E - FR-15, UC-06e)
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class UserStats(BaseModel):
    total: int = Field(..., description="Tổng số người dùng")
    active: int = Field(..., description="Số người dùng đang hoạt động")
    locked: int = Field(..., description="Số người dùng bị khóa (BR-07)")
    new_this_week: int = Field(default=0, description="Số người dùng mới tạo trong 7 ngày qua")


class RestaurantStats(BaseModel):
    total: int = Field(..., description="Tổng số nhà hàng")
    active: int = Field(..., description="Số nhà hàng đang hiển thị / hoạt động")
    hidden: int = Field(..., description="Số nhà hàng tạm ẩn hoặc ngừng hoạt động")
    avg_rating: float = Field(..., description="Điểm đánh giá trung bình toàn hệ thống")


class AISearchTrendItem(BaseModel):
    date: str = Field(..., description="Ngày tìm kiếm (YYYY-MM-DD)")
    search_count: int = Field(..., description="Số lượt tìm kiếm AI ghi nhận trong ngày")


class TopCuisineItem(BaseModel):
    cuisine: str = Field(..., description="Tên thể loại ẩm thực")
    search_count: int = Field(..., description="Số lượt được tìm kiếm qua AI")
    percentage: float = Field(..., description="Tỷ lệ phần trăm trên tổng lượt tìm kiếm có ẩm thực")


class TopFavoritedRestaurantItem(BaseModel):
    id: int = Field(..., description="ID nhà hàng")
    restaurant_id: int = Field(..., description="ID nhà hàng (alias)")
    name: str = Field(..., description="Tên nhà hàng")
    cuisine_type: Optional[str] = Field(None, description="Thể loại ẩm thực")
    address: Optional[str] = Field(None, description="Địa chỉ nhà hàng")
    avg_rating: float = Field(default=0.0, description="Điểm đánh giá trung bình")
    cover_image_url: Optional[str] = Field(None, description="URL ảnh bìa nhà hàng")
    favorite_count: int = Field(..., description="Số lượt được người dùng lưu vào danh sách yêu thích")


class AdminDashboardStatsData(BaseModel):
    users: UserStats
    restaurants: RestaurantStats
    ai_search_trends: List[AISearchTrendItem]
    ai_searches_trend: List[AISearchTrendItem]
    total_ai_searches_in_period: int
    top_cuisines: List[TopCuisineItem]
    top_searched_cuisines: List[TopCuisineItem]
    top_favorited_restaurants: List[TopFavoritedRestaurantItem]
    top_favorites: List[TopFavoritedRestaurantItem]
    reports: Optional[Dict[str, int]] = None
    distributions: Optional[Dict[str, Any]] = None
    admin_info: Optional[Dict[str, Any]] = None


class AdminDashboardStatsResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    data: AdminDashboardStatsData
