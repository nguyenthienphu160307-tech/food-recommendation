from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ReviewBase(BaseModel):
    """Schema cơ bản cho Đánh giá nhà hàng (TSK-51 / FR-10)"""
    rating: int = Field(..., ge=1, le=5, description="Điểm đánh giá từ 1 đến 5 sao")
    comment: Optional[str] = Field(None, max_length=2000, description="Nội dung nhận xét chi tiết")


class ReviewCreateRequest(ReviewBase):
    """Schema yêu cầu gửi đánh giá mới (POST /api/reviews - BR-01, BR-06)"""
    restaurant_id: int = Field(..., description="Mã ID nhà hàng được đánh giá")
    user_id: int = Field(..., description="Mã ID người dùng gửi đánh giá")


class ReviewUpdateRequest(BaseModel):
    """Schema yêu cầu chỉnh sửa đánh giá cũ (PUT /api/reviews/{id} - BR-06)"""
    user_id: int = Field(..., description="Mã ID người dùng sở hữu đánh giá")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Điểm đánh giá mới (1 - 5 sao)")
    comment: Optional[str] = Field(None, max_length=2000, description="Nội dung nhận xét mới")


class ReviewUserSummary(BaseModel):
    """Schema thông tin tóm tắt của người đánh giá"""
    user_id: int
    full_name: str
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReviewResponse(ReviewBase):
    """Schema phản hồi chi tiết một bản ghi đánh giá"""
    id: int = Field(..., description="Mã ID duy nhất của đánh giá")
    restaurant_id: int = Field(..., description="Mã ID nhà hàng")
    user_id: int = Field(..., description="Mã ID người dùng")
    created_at: datetime = Field(..., description="Thời gian tạo đánh giá")
    updated_at: datetime = Field(..., description="Thời gian cập nhật lần cuối")
    user: Optional[ReviewUserSummary] = Field(None, description="Thông tin người dùng đánh giá")

    model_config = ConfigDict(from_attributes=True)


class RestaurantReviewListResponse(BaseModel):
    """Schema phản hồi danh sách đánh giá của nhà hàng kèm thống kê điểm trung bình"""
    restaurant_id: int = Field(..., description="Mã ID nhà hàng")
    restaurant_name: Optional[str] = Field(None, description="Tên nhà hàng")
    avg_rating: float = Field(..., ge=0.0, le=5.0, description="Điểm đánh giá trung bình cập nhật tự động")
    total_reviews: int = Field(..., ge=0, description="Tổng số lượt đánh giá")
    page: int = Field(..., ge=1, description="Trang hiện tại")
    limit: int = Field(..., ge=1, description="Số lượng đánh giá trên mỗi trang")
    items: List[ReviewResponse] = Field(..., description="Danh sách các đánh giá")


class DeleteReviewResponse(BaseModel):
    """Schema phản hồi sau khi xóa đánh giá"""
    success: bool = Field(True, description="Trạng thái xóa thành công")
    message: str = Field(..., description="Thông báo kết quả")
    restaurant_id: int = Field(..., description="Mã ID nhà hàng liên quan")
    avg_rating: float = Field(..., ge=0.0, le=5.0, description="Điểm trung bình sau khi cập nhật lại")
    total_reviews: int = Field(..., ge=0, description="Tổng số đánh giá còn lại")
