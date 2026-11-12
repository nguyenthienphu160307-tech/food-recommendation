from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, model_validator


class CreateSessionRequest(BaseModel):
    """Schema yêu cầu khởi tạo phiên chat mới (Hỗ trợ cả User và Guest)"""
    user_id: Optional[int] = Field(None, description="ID người dùng nếu đã đăng nhập; để trống/None nếu là Khách (Guest)")


class SessionResponse(BaseModel):
    """Schema thông tin phản hồi phiên tìm kiếm / Chat AI"""
    session_id: int
    user_id: Optional[int] = None
    status: str
    started_at: datetime
    total_messages: int = 0

    class Config:
        from_attributes = True


class CloseSessionResponse(BaseModel):
    """Phản hồi khi đóng phiên hội thoại"""
    session_id: int
    status: str
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
    # TSK-20: ID người dùng để áp dụng cài đặt quyền riêng tư (tùy chọn)
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
    # TSK-20: Trả về trạng thái đã làm mờ tọa độ hay chưa
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
