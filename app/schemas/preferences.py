"""
Schemas Pydantic định nghĩa cấu trúc dữ liệu cho:
1. Sở thích cá nhân & Dị ứng thực phẩm (UserPreferences)
2. Kết quả gợi ý nhà hàng cá nhân hóa kèm phân tích giải thích AI (TE9C65C)
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class UserPreferenceBase(BaseModel):
    diet_type: str = Field(
        default="omnivore",
        description="Chế độ ăn: omnivore (bình thường), vegetarian (chay), vegan (thuần chay), halal, keto"
    )
    allergies: List[str] = Field(
        default_factory=list,
        description="Danh sách mã dị ứng: seafood (hải sản), peanut (đậu phộng), dairy (sữa), gluten (lúa mì)..."
    )
    preferred_cuisines: List[str] = Field(
        default_factory=list,
        description="Danh sách thể loại ẩm thực yêu thích: Món Việt, Lẩu Nướng, Món Nhật..."
    )
    avg_budget: Optional[float] = Field(
        default=250000.0,
        ge=0,
        description="Ngân sách ăn uống trung bình ước tính mỗi bữa (VNĐ)"
    )


class UserPreferenceUpdate(BaseModel):
    diet_type: Optional[str] = Field(
        default=None,
        description="Chế độ ăn: omnivore, vegetarian, vegan, halal, keto"
    )
    allergies: Optional[List[str]] = Field(
        default=None,
        description="Danh sách dị ứng thực phẩm"
    )
    preferred_cuisines: Optional[List[str]] = Field(
        default=None,
        description="Danh sách ẩm thực yêu thích"
    )
    avg_budget: Optional[float] = Field(
        default=None,
        ge=0,
        description="Ngân sách ăn uống trung bình (VNĐ)"
    )


class UserPreferenceResponse(BaseModel):
    id: int
    user_id: int
    diet_type: str
    allergies: List[str]
    preferred_cuisines: List[str]
    avg_budget: Optional[float] = 250000.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AppliedPreferencesSummary(BaseModel):
    """Thông tin minh bạch hóa bộ tiêu chí cá nhân hóa mà AI đã áp dụng"""
    is_logged_in: bool
    user_id: Optional[int] = None
    diet_type: Optional[str] = None
    allergies: List[str] = Field(default_factory=list)
    avg_budget: Optional[float] = None
    active_filters: List[str] = Field(default_factory=list)
    filter_reason: str


class RecommendedRestaurantItem(BaseModel):
    id: int
    name: str
    address: str
    cuisine_type: Optional[str] = None
    latitude: float
    longitude: float
    min_price: float
    max_price: float
    avg_rating: float
    total_reviews: int
    status: str
    distance_km: float
    match_score: int
    ai_reason: str
    vegetarian_support: bool = False
    has_parking: bool = False
    has_private_room: bool = False


class RecommendationResponse(BaseModel):
    status: str = "success"
    total: int
    applied_preferences: AppliedPreferencesSummary
    data: List[RecommendedRestaurantItem]
