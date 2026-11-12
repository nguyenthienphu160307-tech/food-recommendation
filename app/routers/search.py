import json
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.chat_session_service import ChatSessionService
from app.services.geocoding_service import GeocodingService
from app.schemas.search import (
    CreateSessionRequest,
    SessionResponse,
    CloseSessionResponse,
    SendMessageRequest,
    MessageResponse,
    SessionHistoryResponse,
    GeocodeRequest,
    GeocodeResponse,
    ExtractCriteriaRequest,
    SearchCriteriaCreateRequest,
    SearchCriteriaResponse,
)

router = APIRouter(prefix="/api/chat", tags=["Trợ lý Chat AI & Geocoding (Module 2 & 3)"])


@router.post(
    "/sessions",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Khởi tạo phiên Chat AI mới (User & Guest - TSK-16)"
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


# =====================================================================
# API GEOCODING & TIÊU CHÍ TÌM KIẾM (TASK TSK-18 / PBI-08)
# =====================================================================

@router.post(
    "/geocode",
    response_model=GeocodeResponse,
    status_code=status.HTTP_200_OK,
    summary="Chuyển đổi tên khu vực/quận sang tọa độ GPS (TSK-18)"
)
def geocode_location(payload: GeocodeRequest):
    """
    API Service Geocoding (Task TSK-18 / PBI-08):
    - Nhận tên địa danh/quận/huyện hoặc trích xuất từ câu tự nhiên.
    - Tra cứu qua Từ điển Tọa độ Nội bộ siêu tốc (< 10ms).
    - Hỗ trợ fallback trực tuyến qua OpenStreetMap khi cần.
    - Trả về cặp tọa độ chuẩn (latitude, longitude) và địa chỉ chuẩn hóa.
    """
    # Nếu người dùng truyền vào cả câu dài (ví dụ: "Tìm quán ở Bình Thạnh"), tự động bóc tách tên địa danh
    extracted_name = GeocodingService.extract_location_from_text(payload.location_name)
    query_target = extracted_name if extracted_name else payload.location_name

    res = GeocodingService.geocode(
        location_name=query_target,
        enable_online_fallback=payload.enable_online_fallback
    )

    return GeocodeResponse(
        location_name=res["location_name"],
        latitude=res["latitude"],
        longitude=res["longitude"],
        formatted_address=res["formatted_address"],
        is_found=res["is_found"],
        source=res["source"]
    )


@router.post(
    "/extract",
    summary="Bóc tách toàn diện tiêu chí (Địa danh, Tọa độ, Ẩm thực, Ngân sách, Tiện ích) từ câu chat"
)
def extract_criteria_from_chat(payload: ExtractCriteriaRequest):
    """
    API bóc tách thực thể ngôn ngữ tự nhiên:
    - Nhận câu chat tiếng Việt.
    - Trích xuất: địa danh, tọa độ GPS (geocoding), món ăn, ngân sách, chỗ đậu xe.
    """
    criteria_data = GeocodingService.extract_full_criteria(payload.message)
    return {
        "status": "success",
        "raw_message": payload.message,
        "criteria": criteria_data
    }


@router.post(
    "/sessions/{session_id}/criteria",
    response_model=SearchCriteriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Lưu hoặc cập nhật tiêu chí tìm kiếm kèm tọa độ GPS vào SearchCriteria (TSK-18)"
)
def save_session_criteria(
    session_id: int,
    payload: SearchCriteriaCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Lưu tiêu chí tìm kiếm vào bảng `SearchCriteria`:
    - Nếu có `location_text` nhưng thiếu `latitude`/`longitude`, tự động gọi GeocodingService để bù tọa độ.
    - Gắn liền với `session_id` để làm tâm bán kính cho Module 3 & 4.
    """
    lat = payload.latitude
    lng = payload.longitude

    # Tự động Geocode nếu chưa có tọa độ
    if payload.location_text and (lat is None or lng is None):
        geo = GeocodingService.geocode(payload.location_text)
        lat = geo["latitude"]
        lng = geo["longitude"]

    crit_obj = ChatSessionService.save_criteria(
        db=db,
        session_id=session_id,
        location_text=payload.location_text,
        latitude=lat,
        longitude=lng,
        cuisine=payload.cuisine,
        budget=payload.budget,
        has_parking=payload.has_parking,
        other_conditions=payload.other_conditions
    )

    return SearchCriteriaResponse(
        criteria_id=crit_obj.criteria_id,
        session_id=crit_obj.session_id,
        location_text=crit_obj.location_text,
        latitude=crit_obj.latitude,
        longitude=crit_obj.longitude,
        cuisine=crit_obj.cuisine,
        budget=crit_obj.budget,
        has_parking=crit_obj.has_parking,
        other_conditions=crit_obj.other_conditions,
        created_at=crit_obj.created_at
    )


@router.get(
    "/sessions/{session_id}/criteria",
    response_model=Optional[SearchCriteriaResponse],
    summary="Lấy tiêu chí tìm kiếm mới nhất của phiên chat"
)
def get_session_criteria(
    session_id: int,
    db: Session = Depends(get_db)
):
    """Truy vấn tiêu chí tìm kiếm hiện tại của phiên chat từ bảng `SearchCriteria`"""
    crit_obj = ChatSessionService.get_latest_criteria(db, session_id)
    if not crit_obj:
        return None

    return SearchCriteriaResponse(
        criteria_id=crit_obj.criteria_id,
        session_id=crit_obj.session_id,
        location_text=crit_obj.location_text,
        latitude=crit_obj.latitude,
        longitude=crit_obj.longitude,
        cuisine=crit_obj.cuisine,
        budget=crit_obj.budget,
        has_parking=crit_obj.has_parking,
        other_conditions=crit_obj.other_conditions,
        created_at=crit_obj.created_at
    )
