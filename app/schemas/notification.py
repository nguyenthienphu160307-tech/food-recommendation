from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class NotificationBase(BaseModel):
    """Schema cơ bản cho thông báo"""
    title: str = Field(..., min_length=1, max_length=255, description="Tiêu đề thông báo")
    content: str = Field(..., min_length=1, description="Nội dung chi tiết thông báo")
    type: str = Field("system", max_length=50, description="Loại thông báo ('system', 'review_reply', 'account_status', 'review_moderation')")


class NotificationCreateRequest(NotificationBase):
    """Schema yêu cầu tạo thông báo mới cho người dùng cụ thể"""
    user_id: int = Field(..., description="ID người nhận thông báo")


class NotificationBroadcastRequest(NotificationBase):
    """Schema yêu cầu gửi thông báo hàng loạt (Broadcast)"""
    user_ids: Optional[List[int]] = Field(None, description="Danh sách ID người nhận (Nếu None, gửi đến tất cả người dùng active)")


class NotificationResponse(NotificationBase):
    """Schema phản hồi chi tiết một bản ghi thông báo"""
    id: int = Field(..., description="Mã ID duy nhất của thông báo")
    user_id: int = Field(..., description="Mã ID người nhận")
    is_read: bool = Field(..., description="Trạng thái đã đọc (True: Đã đọc, False: Chưa đọc)")
    created_at: datetime = Field(..., description="Thời gian khởi tạo thông báo")

    model_config = ConfigDict(from_attributes=True)


class NotificationListResponse(BaseModel):
    """Schema phản hồi danh sách thông báo kèm phân trang và số lượng chưa đọc"""
    total: int = Field(..., description="Tổng số thông báo")
    unread_count: int = Field(..., description="Số lượng thông báo chưa đọc")
    page: int = Field(..., ge=1, description="Trang hiện tại")
    limit: int = Field(..., ge=1, description="Số lượng mục trên mỗi trang")
    items: List[NotificationResponse] = Field(..., description="Danh sách thông báo")


class UnreadCountResponse(BaseModel):
    """Schema phản hồi số lượng thông báo chưa đọc"""
    user_id: int = Field(..., description="ID người dùng")
    unread_count: int = Field(..., ge=0, description="Số lượng thông báo chưa đọc")


class MarkReadResponse(BaseModel):
    """Schema phản hồi sau khi đánh dấu đã đọc"""
    success: bool = Field(True, description="Trạng thái xử lý thành công")
    message: str = Field(..., description="Thông báo kết quả")
    updated_count: int = Field(..., ge=0, description="Số lượng bản ghi thông báo đã được cập nhật")


class ReviewReplyNotificationRequest(BaseModel):
    """Schema trigger thông báo khi nhận phản hồi đánh giá quán ăn"""
    user_id: int = Field(..., description="ID người dùng nhận thông báo (chủ đánh giá)")
    restaurant_name: str = Field(..., description="Tên nhà hàng được phản hồi")
    reviewer_name: str = Field(..., description="Tên người phản hồi hoặc chủ nhà hàng")
    reply_content: str = Field(..., description="Nội dung tóm tắt của phản hồi")


class AccountStatusNotificationRequest(BaseModel):
    """Schema trigger thông báo khi trạng thái tài khoản thay đổi (active / locked)"""
    user_id: int = Field(..., description="ID người dùng")
    new_status: str = Field(..., description="Trạng thái mới của tài khoản ('active', 'locked')")
    reason: Optional[str] = Field(None, description="Lý do khóa hoặc mở khóa tài khoản")
