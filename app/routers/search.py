from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.chat_session_service import ChatSessionService
from app.schemas.search import (
    CreateSessionRequest,
    SessionResponse,
    CloseSessionResponse,
    SendMessageRequest,
    MessageResponse,
    SessionHistoryResponse,
)

router = APIRouter(prefix="/api/chat", tags=["Trợ lý Chat AI & Phiên tìm kiếm (Module 2)"])


@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Khởi tạo phiên Chat AI mới (User & Guest)"
)
def create_session(
    payload: Optional[CreateSessionRequest] = None,
    db: Session = Depends(get_db)
):
    """
    API Khởi tạo phiên chat tìm kiếm quán ăn (TSK-16):
    - Hỗ trợ User đã đăng nhập (truyền `user_id`).
    - Hỗ trợ Khách vãng lai (`user_id = None` theo quy tắc BR-02).
    - Tạo bản ghi mới trong bảng `SearchSessions` với trạng thái `active`.
    """
    user_id = payload.user_id if payload else None
    session_obj = ChatSessionService.create_session(db, user_id=user_id)
    return SessionResponse(
        session_id=session_obj.session_id,
        user_id=session_obj.user_id,
        status=session_obj.status,
        started_at=session_obj.started_at,
        total_messages=0
    )


@router.get(
    "/sessions/{session_id}",
    response_model=SessionHistoryResponse,
    summary="Lấy chi tiết phiên và toàn bộ lịch sử tin nhắn theo thứ tự thời gian"
)
def get_session_history(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin phiên chat và danh sách toàn bộ tin nhắn đã trao đổi:
    - Sắp xếp tăng dần theo thời gian thực (created_at ASC).
    - Phân biệt rõ tin nhắn người dùng (sender_type='user') và trợ lý ảo (sender_type='ai').
    """
    session_obj = ChatSessionService.get_session(db, session_id)
    messages = ChatSessionService.get_session_messages(db, session_id)

    return SessionHistoryResponse(
        session=SessionResponse(
            session_id=session_obj.session_id,
            user_id=session_obj.user_id,
            status=session_obj.status,
            started_at=session_obj.started_at,
            total_messages=len(messages)
        ),
        messages=[
            MessageResponse(
                message_id=m.message_id,
                session_id=m.session_id,
                sender_type=m.sender_type,
                content=m.content,
                created_at=m.created_at
            )
            for m in messages
        ]
    )


@router.post(
    "/sessions/{session_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Lưu tin nhắn mới vào phiên chat theo thời gian thực"
)
def send_message(
    session_id: int,
    payload: SendMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Lưu trữ tin nhắn vào bảng `SearchMessages`:
    - Ghi nhận ngay lập tức theo thời gian thực.
    - Chặn gửi tin nhắn nếu phiên đã ở trạng thái 'closed' (HTTP 400).
    """
    msg_obj = ChatSessionService.save_message(
        db=db,
        session_id=session_id,
        sender_type=payload.sender_type,
        content=payload.content
    )
    return MessageResponse(
        message_id=msg_obj.message_id,
        session_id=msg_obj.session_id,
        sender_type=msg_obj.sender_type,
        content=msg_obj.content,
        created_at=msg_obj.created_at
    )


@router.put(
    "/sessions/{session_id}/close",
    response_model=CloseSessionResponse,
    summary="Đóng phiên hội thoại chat (status='closed')"
)
def close_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Chuyển trạng thái phiên sang 'closed':
    - Được gọi khi người dùng đã tìm được quán ưng ý hoặc kết thúc phiên hội thoại.
    """
    session_obj = ChatSessionService.close_session(db, session_id)
    return CloseSessionResponse(
        session_id=session_obj.session_id,
        status=session_obj.status,
        message=f"Phiên chat #{session_id} đã được đóng thành công."
    )


@router.get(
    "/sessions",
    response_model=List[SessionResponse],
    summary="Lấy danh sách các phiên chat gần đây"
)
def list_sessions(
    user_id: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lấy danh sách các phiên chat gần nhất (hỗ trợ lọc theo user_id)"""
    sessions = ChatSessionService.list_sessions(db, user_id=user_id, limit=limit)
    return [
        SessionResponse(
            session_id=s.session_id,
            user_id=s.user_id,
            status=s.status,
            started_at=s.started_at,
            total_messages=len(s.messages) if s.messages else 0
        )
        for s in sessions
    ]
