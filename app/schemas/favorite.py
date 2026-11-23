from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.restaurant import RestaurantListItemResponse, PaginationMetadata


class FavoriteCreateRequest(BaseModel):
    """
    Yêu cầu lưu nhà hàng vào danh sách yêu thích (Task TE9C67D / FR-11, UC-08):
    - restaurant_id: ID nhà hàng hợp lệ (bắt buộc)
    - note: Ghi chú cá nhân về nhà hàng (tùy chọn, tối đa 255 ký tự)
    - user_id: ID người dùng tùy chọn (hỗ trợ gọi trực tiếp trong unit test)
    """
    restaurant_id: int = Field(..., ge=1, description="ID nhà hàng cần thêm vào danh sách yêu thích")
    note: Optional[str] = Field(None, max_length=255, description="Ghi chú cá nhân về nhà hàng (tùy chọn)")
    user_id: Optional[int] = Field(None, description="ID người dùng (tùy chọn)")


class FavoriteDeleteRequest(BaseModel):
    """Yêu cầu bỏ lưu nhà hàng khỏi danh sách yêu thích"""
    restaurant_id: Optional[int] = Field(None, ge=1, description="ID nhà hàng cần bỏ lưu")
    user_id: Optional[int] = Field(None, description="ID người dùng (tùy chọn)")


class FavoriteItemResponse(BaseModel):
    """Thông tin một mục nhà hàng yêu thích kèm thông tin nhà hàng chi tiết"""
    favorite_id: int = Field(..., description="ID bản ghi yêu thích")
    restaurant_id: int = Field(..., description="ID nhà hàng")
    user_id: int = Field(..., description="ID người dùng sở hữu")
    note: Optional[str] = Field(None, description="Ghi chú cá nhân của người dùng")
    created_at: datetime = Field(..., description="Thời gian lưu vào danh sách yêu thích")
    restaurant: RestaurantListItemResponse = Field(..., description="Thông tin chi tiết nhà hàng")

    model_config = ConfigDict(from_attributes=True)


class FavoriteListResponse(BaseModel):
    """Phản hồi danh sách nhà hàng yêu thích có phân trang (FR-11, UC-08)"""
    status: str = Field(default="success", description="Trạng thái phản hồi ('success')")
    task_code: str = Field(default="TE9C67D", description="Mã task thực thi")
    total: int = Field(..., description="Tổng số nhà hàng trong danh sách yêu thích")
    data: List[FavoriteItemResponse] = Field(default_factory=list, description="Danh sách các mục yêu thích")
    pagination: PaginationMetadata = Field(..., description="Metadata phân trang chuẩn RESTful")


class FavoriteActionResponse(BaseModel):
    """Phản hồi kết quả thao tác lưu hoặc bỏ lưu nhà hàng yêu thích"""
    status: str = Field(default="success", description="Trạng thái phản hồi")
    task_code: str = Field(default="TE9C67D", description="Mã task thực thi")
    message: str = Field(..., description="Thông điệp phản hồi cho người dùng")
    favorite_id: Optional[int] = Field(None, description="ID bản ghi yêu thích nếu vừa tạo mới")
    restaurant_id: int = Field(..., description="ID nhà hàng")
    is_favorite: bool = Field(..., description="Trạng thái yêu thích hiện tại (True: đã lưu, False: chưa lưu)")


class FavoriteCheckResponse(BaseModel):
    """Phản hồi kiểm tra trạng thái nhà hàng đã được yêu thích hay chưa"""
    restaurant_id: int = Field(..., description="ID nhà hàng kiểm tra")
    is_favorite: bool = Field(..., description="Trạng thái yêu thích (True/False)")
    favorite_id: Optional[int] = Field(None, description="ID bản ghi yêu thích nếu có")
    note: Optional[str] = Field(None, description="Ghi chú nếu có")
    created_at: Optional[datetime] = Field(None, description="Thời gian lưu nếu có")
