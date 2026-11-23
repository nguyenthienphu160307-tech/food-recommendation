from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, model_validator


class CreateSessionRequest(BaseModel):
    """Schema yêu cầu khởi tạo phiên chat mới (Hỗ trợ cả User và Guest)"""
    user_id: Optional[int] = Field(None, description="ID người dùng nếu đã đăng nhập; để trống/None nếu là Khách (Guest)")


class SessionResponse(BaseModel):
    """Schema thông tin phản hồi phiên tìm kiếm / Chat AI (TSK-16 / TSK-45)"""
    session_id: int
    user_id: Optional[int] = None
    status: str
    current_state: str = "SESSION_IDLE"
    started_at: datetime
    ended_at: Optional[datetime] = None
    closed_reason: Optional[str] = None
    total_messages: int = 0
    title_preview: Optional[str] = Field(None, description="Tiêu đề tóm tắt cuộc trò chuyện (trích từ câu hỏi đầu của user)")
    last_message_at: Optional[datetime] = Field(None, description="Thời gian tin nhắn cuối cùng trong phiên")

    class Config:
        from_attributes = True


class CloseSessionRequest(BaseModel):
    """Yêu cầu đóng phiên tìm kiếm / hội thoại chat (TE9C66C)"""
    reason: Optional[str] = Field(
        "user_ended",
        description="Lý do đóng phiên: 'user_ended', 'restaurant_selected', 'timeout', 'manual'"
    )
    selected_restaurant_id: Optional[int] = Field(
        None,
        description="ID nhà hàng đã chọn nếu kết thúc phiên bằng việc chốt quán"
    )
    note: Optional[str] = Field(
        None,
        description="Ghi chú thêm từ người dùng khi đóng phiên"
    )


class CloseSessionResponse(BaseModel):
    """Phản hồi khi đóng phiên hội thoại (TE9C66C)"""
    session_id: int
    status: str
    current_state: str = "SESSION_CLOSED"
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    closed_reason: Optional[str] = None
    selected_restaurant_id: Optional[int] = None
    total_messages: int = 0
    message: str


class SessionStatusResponse(BaseModel):
    """Chi tiết trạng thái phiên tìm kiếm và thông số thời gian hoạt động (TE9C66C)"""
    session_id: int
    user_id: Optional[int] = None
    status: str
    current_state: str
    is_active: bool
    is_timed_out: bool
    started_at: datetime
    last_activity_at: datetime
    ended_at: Optional[datetime] = None
    idle_seconds: float
    duration_seconds: Optional[float] = None
    closed_reason: Optional[str] = None
    total_messages: int = 0


class TimeoutCleanupRequest(BaseModel):
    """Yêu cầu quét và đóng các phiên hết thời gian chờ (TE9C66C)"""
    timeout_minutes: Optional[int] = Field(
        None,
        ge=1,
        le=1440,
        description="Ngưỡng phút không hoạt động để tính timeout (mặc định cấu hình hệ thống: 30 phút)"
    )


class TimeoutCleanupResponse(BaseModel):
    """Kết quả sau khi quét và đóng các phiên hết thời gian chờ (TE9C66C)"""
    closed_count: int
    closed_session_ids: List[int]
    timeout_minutes: int
    message: str


class SendMessageRequest(BaseModel):
    """Schema gửi tin nhắn mới vào phiên chat theo thời gian thực"""
    content: str = Field(..., min_length=1, description="Nội dung tin nhắn")
    sender_type: str = Field("user", description="Loại người gửi: 'user' hoặc 'ai'")

    @model_validator(mode="after")
    def validate_sender(self):
        self.content = self.content.strip()
        if not self.content:
            raise ValueError("Nội dung tin nhắn không được để trống.")
        sender = self.sender_type.lower().strip()
        if sender not in ("user", "ai"):
            raise ValueError("Loại người gửi phải là 'user' hoặc 'ai'.")
        self.sender_type = sender
        return self


class MessageResponse(BaseModel):
    """Schema chi tiết một tin nhắn trong phiên chat"""
    message_id: int
    session_id: int
    sender_type: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class SessionHistoryResponse(BaseModel):
    """Schema toàn bộ lịch sử tin nhắn của một phiên chat theo thời gian thực"""
    session: SessionResponse
    messages: List[MessageResponse]


# =====================================================================
# SCHEMAS CHO SERVICE GEOCODING & SEARCH CRITERIA (TASK TSK-18)
# =====================================================================

class GeocodeRequest(BaseModel):
    """Yêu cầu chuyển đổi tên khu vực / quận sang tọa độ GPS"""
    location_name: str = Field(..., min_length=1, description="Tên địa danh, quận/huyện hoặc câu chat có chứa địa danh")
    enable_online_fallback: bool = Field(True, description="Cho phép fallback sang OpenStreetMap khi không có trong từ điển nội bộ")


class GeocodeResponse(BaseModel):
    """Phản hồi kết quả Geocoding"""
    location_name: str
    latitude: float
    longitude: float
    formatted_address: str
    is_found: bool
    source: str


class ExtractCriteriaRequest(BaseModel):
    """Yêu cầu trích xuất tiêu chí và tọa độ từ câu chat tự nhiên"""
    message: str = Field(..., min_length=1, description="Câu chat tự nhiên tiếng Việt")


class SearchCriteriaCreateRequest(BaseModel):
    """Yêu cầu lưu tiêu chí tìm kiếm kèm tọa độ GPS vào SearchCriteria"""
    location_text: Optional[str] = Field(None, description="Tên khu vực / quận gốc")
    latitude: Optional[float] = Field(None, description="Vĩ độ tâm tìm kiếm")
    longitude: Optional[float] = Field(None, description="Kinh độ tâm tìm kiếm")
    cuisine: Optional[str] = Field(None, description="Loại ẩm thực (lẩu, nướng, chay...)")
    budget: Optional[int] = Field(None, description="Ngân sách dự kiến (VND)")
    has_parking: Optional[bool] = Field(False, description="Yêu cầu bãi đỗ xe")
    other_conditions: Optional[str] = Field(None, description="Điều kiện mở rộng định dạng JSON text")
    user_id: Optional[int] = Field(None, description="ID người dùng để áp dụng cơ chế bảo vệ quyền riêng tư GPS")
    is_obfuscated: Optional[bool] = Field(False, description="Đánh dấu tọa độ đã được làm mờ theo cơ chế BR-08")


class SearchCriteriaResponse(BaseModel):
    """Phản hồi tiêu chí tìm kiếm đã lưu trong CSDL"""
    criteria_id: int
    session_id: int
    location_text: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cuisine: Optional[str] = None
    budget: Optional[int] = None
    has_parking: Optional[bool] = False
    other_conditions: Optional[str] = None
    is_obfuscated: Optional[bool] = False
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================================
# SCHEMAS QUYỀN RIÊNG TƯ VỊ TRÍ GPS (TASK TSK-20 / BR-08, NFR-07)
# =====================================================================

class PrivacySettingsResponse(BaseModel):
    """Phản hồi cài đặt quyền riêng tư vị trí GPS hiện tại của người dùng"""
    user_id: int
    share_exact_location: bool = False
    auto_purge_location: bool = True
    profile_exists: bool = True


class PrivacySettingsUpdateRequest(BaseModel):
    """Yêu cầu cập nhật cài đặt quyền riêng tư vị trí GPS"""
    user_id: int = Field(..., description="ID người dùng cần cập nhật cài đặt")
    share_exact_location: Optional[bool] = Field(
        None,
        description="True = chia sẻ tọa độ chính xác; False (mặc định) = chỉ chia sẻ khu vực xấp xỉ ~1,1km"
    )
    auto_purge_location: Optional[bool] = Field(
        None,
        description="True (mặc định) = tự động xóa log tọa độ sau khi đóng phiên chat"
    )


class PurgeLocationResponse(BaseModel):
    """Phản hồi sau khi thực hiện xóa log tọa độ của một phiên chat"""
    session_id: int
    purged_count: int
    message: str


# =====================================================================
# SCHEMAS XÓA NHANH TIÊU CHÍ ĐÃ BÓC TÁCH (TASK TE9C673)
# =====================================================================

class RemoveCriterionRequest(BaseModel):
    """Yêu cầu xóa nhanh một tiêu chí khỏi SearchCriteria (TE9C673)"""
    field: str = Field(
        ...,
        description="Tên trường tiêu chí cần xóa: 'location', 'cuisine', 'budget', 'has_parking', 'has_private_room', 'has_outdoor', 'has_pet_friendly', 'vegetarian', hoặc 'all'"
    )


class RemoveCriterionResponse(BaseModel):
    """Phản hồi sau khi xóa nhanh tiêu chí và cập nhật danh sách nhà hàng (TE9C673)"""
    session_id: int
    removed_field: str
    status: str = "success"
    ai_message: str
    updated_criteria: Optional[Dict[str, Any]] = None
    results: List[Dict[str, Any]] = Field(default_factory=list)
    total_found: int = 0


# =====================================================================
# SCHEMAS LỊCH SỬ TÌM KIẾM & GỢI Ý NHÀ HÀNG (TASK TSK-46 / TE9C677)
# =====================================================================

class SuggestedRestaurantHistoryItem(BaseModel):
    """Thông tin nhà hàng được gợi ý lại trong một phiên tìm kiếm cũ"""
    id: int
    name: str
    address: Optional[str] = None
    cuisine_type: Optional[str] = None
    avg_rating: float = 4.5
    min_price: float = 0.0
    max_price: float = 0.0
    cover_image_url: Optional[str] = None
    is_open: bool = True
    match_score: int = 85
    distance_km: Optional[float] = None


class SearchHistorySessionItem(BaseModel):
    """Chi tiết một phiên tìm kiếm cũ kèm tiêu chí và danh sách quán đã gợi ý"""
    session_id: int
    user_id: Optional[int] = None
    status: str
    started_at: datetime
    title_preview: str
    total_messages: int = 0
    criteria: Optional[SearchCriteriaResponse] = None
    suggested_restaurants: List[SuggestedRestaurantHistoryItem] = Field(default_factory=list)


class SearchHistoryResponse(BaseModel):
    """Phản hồi danh sách lịch sử tìm kiếm có phân trang"""
    total_sessions: int
    page: int
    limit: int
    total_pages: int
    data: List[SearchHistorySessionItem]