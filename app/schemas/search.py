from datetime import datetime
from typing import Optional, List
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
